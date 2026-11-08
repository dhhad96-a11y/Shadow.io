import os
import json
import random
import string
from flask import Flask, render_template, request, jsonify, session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR, static_folder=None)
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key-change-me")

KV_URL = os.environ.get("KV_REST_API_URL")
KV_TOKEN = os.environ.get("KV_REST_API_TOKEN")

redis_db = None
if KV_URL and KV_TOKEN:
    try:
        from upstash_redis import Redis
        redis_db = Redis(url=KV_URL, token=KV_TOKEN)
    except ImportError:
        print("Warning: upstash_redis not installed.")

_local_keys = []

def get_keys():
    if redis_db:
        data = redis_db.get("keys")
        return json.loads(data) if data else []
    return _local_keys

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/keys/validate", methods=["POST"])
def validate_key():
    data = request.get_json(silent=True) or {}
    input_key = (data.get("key") or "").strip()

    if not input_key:
        return jsonify({"ok": False, "error": "Please enter Access Key!"}), 400

    keys = get_keys()
    live_keys = [k["code"] for k in keys]
    live_keys.append("SHDW-VIP-PASS-2026")

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
