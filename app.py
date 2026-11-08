import os
import json
import random
import string
from flask import Flask, render_template, request, jsonify, session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR, static_folder=None)
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key-change-me")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "SHADOW V2")

# ============================================================
# 🗄️ إعداد قاعدة البيانات السحابية (Vercel KV / Upstash)
# ============================================================
KV_URL = os.environ.get("KV_REST_API_URL")
KV_TOKEN = os.environ.get("KV_REST_API_TOKEN")

redis_db = None
if KV_URL and KV_TOKEN:
    try:
        from upstash_redis import Redis
        redis_db = Redis(url=KV_URL, token=KV_TOKEN)
    except ImportError:
        print("Warning: upstash_redis not installed.")

# ذاكرة مؤقتة (تستخدم فقط إذا لم تكن قاعدة البيانات متصلة أثناء التجربة المحلية)
_local_resellers = []
_local_keys = []
_id_state = {"next": 1}

def _new_id():
    _id_state["next"] += 1
    return f"r{_id_state['next']}"

def get_resellers():
    if redis_db:
        data = redis_db.get("resellers")
        return json.loads(data) if data else []
    return _local_resellers

def save_resellers(data):
    if redis_db:
        redis_db.set("resellers", json.dumps(data))
    else:
        global _local_resellers
        _local_resellers = data

def get_keys():
    if redis_db:
        data = redis_db.get("keys")
        return json.loads(data) if data else []
    return _local_keys

def save_keys(data):
    if redis_db:
        redis_db.set("keys", json.dumps(data))
    else:
        global _local_keys
        _local_keys = data

# ============================================================
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or {}
    password = (data.get("password") or "").strip()

    if password == ADMIN_PASSWORD or password == ADMIN_PASSWORD.lower():
        session["role"] = "admin"
        return jsonify({"ok": True, "role": "admin", "title": "👑 Control Panel", "balance": "UNLIMITED"})
    return jsonify({"ok": False, "error": "Access Denied!"}), 401

@app.route("/api/reseller/login", methods=["POST"])
def reseller_login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip().lower()
    resellers = get_resellers()

    for r in resellers:
        if r["name"].lower() == username:
            session["role"] = "reseller"
            session["reseller_id"] = r["id"]
            return jsonify({"ok": True, "role": "reseller", "title": f"👤 Seller: {r['name']}", "balance": f"${r['balance']:.2f}"})
    return jsonify({"ok": False, "error": "User not found!"}), 404

@app.route("/api/resellers", methods=["GET"])
def list_resellers():
    if session.get("role") != "admin":
        return jsonify({"ok": False, "error": "Unauthorized"}), 403
    return jsonify({"ok": True, "resellers": get_resellers()})

@app.route("/api/resellers", methods=["POST"])
def add_reseller():
    if session.get("role") != "admin":
        return jsonify({"ok": False, "error": "Unauthorized"}), 403

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    try:
        balance = float(data.get("balance") or 0)
    except (TypeError, ValueError):
        balance = 0.0

    resellers = get_resellers()
    if not name:
        return jsonify({"ok": False, "error": "Please enter username"}), 400
    if any(r["name"].lower() == name.lower() for r in resellers):
        return jsonify({"ok": False, "error": "Username already exists!"}), 409

    new_reseller = {"id": _new_id(), "name": name, "balance": balance}
    resellers.append(new_reseller)
    save_resellers(resellers)
    
    return jsonify({"ok": True, "reseller": new_reseller, "resellers": resellers})

@app.route("/api/resellers/<rid>", methods=["DELETE"])
def delete_reseller(rid):
    if session.get("role") != "admin":
        return jsonify({"ok": False, "error": "Unauthorized"}), 403

    resellers = get_resellers()
    before = len(resellers)
    resellers = [r for r in resellers if r["id"] != rid]
    if len(resellers) == before:
        return jsonify({"ok": False, "error": "Not found"}), 404
        
    save_resellers(resellers)
    return jsonify({"ok": True, "resellers": resellers})

@app.route("/api/keys/generate", methods=["POST"])
def generate_key():
    role = session.get("role")
    if role not in ("admin", "reseller"):
        return jsonify({"ok": False, "error": "Unauthorized"}), 403

    data = request.get_json(silent=True) or {}
    try:
        price = float(data.get("price") or 0)
    except (TypeError, ValueError):
        price = 0.0

    new_balance = "UNLIMITED"
    
    if role == "reseller":
        rid = session.get("reseller_id")
        resellers = get_resellers()
        target = next((r for r in resellers if r["id"] == rid), None)
        
        if not target:
            return jsonify({"ok": False, "error": "Reseller not found"}), 404
        if target["balance"] < price:
            return jsonify({"ok": False, "error": "❌ Insufficient balance!"}), 400
            
        target["balance"] -= price
        save_resellers(resellers)
        new_balance = f"${target['balance']:.2f}"

    chars = string.ascii_uppercase + string.digits
    key = "SHDW-"
    for j in range(12):
        key += random.choice(chars)
        if j == 3 or j == 7:
            key += "-"

    keys = get_keys()
    keys.append({"code": key})
    save_keys(keys)
    
    return jsonify({"ok": True, "key": key, "balance": new_balance})

@app.route("/api/keys/validate", methods=["POST"])
def validate_key():
    data = request.get_json(silent=True) or {}
    input_key = (data.get("key") or "").strip()

    if not input_key:
        return jsonify({"ok": False, "error": "Please enter Access Key!"}), 400

    keys = get_keys()
    live_keys = [k["code"] for k in keys]
    live_keys.append("SHDW-VIP-PASS-2026") # مفتاح احتياطي دائم

    if input_key in live_keys:
        session["role"] = "user"
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "❌ ERROR: Invalid or expired key!"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)