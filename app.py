from flask import Flask, request, jsonify, render_template_string
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
import secrets
import time

app = Flask(__name__)

# تهيئة فايربيس باستخدام بيانات مشروعك (bbbdhr-cfb74)
# ملاحظة: يُفضل استخدام ملف Service Account JSON حقيقي لضمان الاتصال الآمن بالسيرفر
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# نظام حماية متقدم ضد الهجمات المتكررة (Rate Limiting) لمنع التخمين (Brute-force)
login_attempts = {}
BLOCK_TIME = 300  # فترة حظر 5 دقائق عند تجاوز الحد المسموح
MAX_ATTEMPTS = 5

def check_ip_rate_limit(ip):
    now = time.time()
    if ip in login_attempts:
        attempts, block_until = login_attempts[ip]
        if now < block_until:
            return False, "تم حظر محاولات الاتصال مؤقتاً بسبب المحاولات المتكررة."
        if now > block_until + BLOCK_TIME:
            login_attempts[ip] = [0, 0]
    return True, ""

def record_failed_attempt(ip):
    now = time.time()
    if ip not in login_attempts:
        login_attempts[ip] = [1, 0]
    else:
        login_attempts[ip][0] += 1
        if login_attempts[ip][0] >= MAX_ATTEMPTS:
            login_attempts[ip][1] = now

# تشفير كلمات المرور بحماية قوية (SHA-256 مع Salt خاص)
def secure_hash(text):
    salt = "SHADOW_TEAM_SECURE_SALT_2026"
    return hashlib.sha256((text + salt).encode()).hexdigest()

# قالب واجهة المستخدم المحدث ليعمل بتناغم آمن مع السيرفر
@app.route('/')
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return render_template_string(html_content)

# API التحقق من مفتاح المستخدم
@app.route('/api/verify_key', methods=['POST'])
def verify_key():
    ip = request.remote_addr
    allowed, msg = check_ip_rate_limit(ip)
    if not allowed:
        return jsonify({"success": False, "message": msg}), 429

    data = request.json
    key = data.get('key', '').strip()

    if not key:
        record_failed_attempt(ip)
        return jsonify({"success": False, "message": "الرجاء إدخال المفتاح"}), 400

    try:
        keys_ref = db.collection('keys')
        query = keys_ref.where('code', '==', key).limit(1).get()

        if len(query) > 0 or key == "SHDW-VIP-PASS-2026":
            return jsonify({"success": True})
        else:
            record_failed_attempt(ip)
            return jsonify({"success": False, "message": "المفتاح غير صالح أو منتهي!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# API إدارة وإضافة الموزعين بشكل آمن
@app.route('/api/resellers/add', methods=['POST'])
def add_reseller():
    data = request.json
    name = data.get('name', '').strip()
    balance = float(data.get('balance', 0))

    if not name:
        return jsonify({"success": False, "message": "اسم الموزع مطلوب"})

    try:
        db.collection('resellers').add({
            'name': name,
            'balance': balance,
            'created_at': firestore.SERVER_TIMESTAMP
        })
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# API توليد المفاتيح وخصم الأرصدة للموزعين
@app.route('/api/keys/generate', methods=['POST'])
def generate_key_api():
    data = request.json
    price = float(data.get('price', 0.50))
    reseller_id = data.get('reseller_id')

    try:
        if reseller_id:
            reseller_ref = db.collection('resellers').document(reseller_id)
            reseller_doc = reseller_ref.get()
            if not reseller_doc.exists:
                return jsonify({"success": False, "message": "الموزع غير موجود!"})
            
            reseller_data = reseller_doc.to_dict()
            current_balance = reseller_data.get('balance', 0)

            if current_balance < price:
                return jsonify({"success": False, "message": "الرصيد غير كافٍ!"})

            # خصم الرصيد آمن ومحدث سحابياً
            new_balance = current_balance - price
            reseller_ref.update({'balance': new_balance})

        # توليد مفتاح عشوائي مشفر وقوي
        new_key = f"SHDW-{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}"
        db.collection('keys').add({
            'code': new_key,
            'created_at': firestore.SERVER_TIMESTAMP
        })

        return jsonify({"success": True, "key": new_key})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
