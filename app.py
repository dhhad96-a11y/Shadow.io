from flask import Flask, request, jsonify, session, render_template_string
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

ADMIN_PASSWORD = "ADHAM SHADOW"

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyCc-8w0G8AIxEpoScTC3eqs0rcdDWd-j8g",
    "authDomain": "wbbhdh-9ede6.firebaseapp.com",
    "projectId": "wbbhdh-9ede6",
    "storageBucket": "wbbhdh-9ede6.firebasestorage.app",
    "messagingSenderId": "426376855325",
    "appId": "1:426376855325:android:30a926985465c34d16abf4"
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Shadow - AimBot & VPN Panel</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: #090a0f;
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow-x: hidden;
            position: relative;
        }

        #particleCanvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
        }

        .screen {
            display: none;
            width: 100%;
            max-width: 390px;
            position: relative;
            z-index: 1;
            animation: fadeIn 0.35s ease-in-out;
        }
        .screen.active {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .main-card {
            width: 100%;
            background: #13151b;
            border: 1px solid #1f232d;
            border-radius: 26px;
            padding: 36px 24px 28px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75);
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .shield-box {
            width: 68px;
            height: 68px;
            background: linear-gradient(145deg, #1d2230, #161923);
            border: 1px solid #292f42;
            border-radius: 18px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        }

        .shield-svg {
            width: 34px;
            height: 34px;
            fill: #00e676;
        }

        .brand-title {
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
            color: #ffffff;
        }
        .brand-title span {
            color: #00e676;
        }

        .brand-subtitle {
            font-size: 10px;
            font-weight: 700;
            color: #7d8597;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 26px;
        }

        .input-wrapper {
            width: 100%;
            position: relative;
            margin-bottom: 16px;
        }

        .pass-input {
            width: 100%;
            background: #0d0e12;
            border: 1px solid #1a1d26;
            border-radius: 14px;
            padding: 15px 40px;
            color: #ffffff;
            font-size: 13px;
            text-align: center;
            outline: none;
            transition: border-color 0.25s;
        }
        .pass-input::placeholder {
            color: #6c7385;
            font-weight: 600;
        }
        .pass-input:focus {
            border-color: #00e676;
        }

        .green-btn {
            width: 100%;
            background: #00e676;
            color: #041a0c;
            border: none;
            border-radius: 14px;
            padding: 15px;
            font-size: 14px;
            font-weight: 800;
            letter-spacing: 1px;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            box-shadow: 0 6px 22px rgba(0, 230, 118, 0.35);
            transition: all 0.25s ease;
        }
        .green-btn:hover {
            background: #00f27d;
            transform: translateY(-1px);
            box-shadow: 0 8px 26px rgba(0, 230, 118, 0.5);
        }

        /* زر Aim Bot المميز */
        .aimbot-panel-btn {
            width: 100%;
            background: linear-gradient(135deg, #ff3b30, #ff9500);
            color: #ffffff;
            border: none;
            border-radius: 14px;
            padding: 16px;
            font-size: 15px;
            font-weight: 900;
            letter-spacing: 1px;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
            box-shadow: 0 8px 25px rgba(255, 59, 48, 0.4);
            animation: pulseGlow 2s infinite;
        }
        @keyframes pulseGlow {
            0% { box-shadow: 0 0 15px rgba(255, 59, 48, 0.4); }
            50% { box-shadow: 0 0 30px rgba(255, 149, 0, 0.7); }
            100% { box-shadow: 0 0 15px rgba(255, 59, 48, 0.4); }
        }

        .footer-pill {
            margin-top: 22px;
            background: rgba(0, 230, 118, 0.08);
            border: 1px solid rgba(0, 230, 118, 0.22);
            border-radius: 999px;
            padding: 8px 18px;
            font-size: 11px;
            font-weight: 700;
            color: #00e676;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .dash-card {
            padding: 24px 20px;
            text-align: left;
            max-height: 92vh;
            overflow-y: auto;
        }

        .dash-top {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 14px;
            margin-bottom: 16px;
            border-bottom: 1px solid #1f232d;
        }

        .dash-user {
            font-size: 14px;
            font-weight: 800;
            color: #ffffff;
        }

        .section-heading {
            width: 100%;
            font-size: 12px;
            font-weight: 800;
            color: #00e676;
            margin: 14px 0 8px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .field-label {
            width: 100%;
            font-size: 11px;
            color: #7d8597;
            margin-bottom: 5px;
            font-weight: 600;
        }

        .dark-input, .dark-select {
            width: 100%;
            background: #0d0e12;
            border: 1px solid #1f232d;
            border-radius: 12px;
            padding: 12px 14px;
            color: #ffffff;
            font-size: 13px;
            margin-bottom: 12px;
            outline: none;
        }
        .dark-input:focus, .dark-select:focus {
            border-color: #00e676;
        }

        .result-box {
            width: 100%;
            background: #0d0e12;
            border: 1px dashed #00e676;
            border-radius: 14px;
            padding: 16px;
            margin-top: 16px;
            text-align: center;
        }

        .key-display {
            font-family: monospace;
            font-size: 15px;
            font-weight: 800;
            color: #00e676;
            margin: 6px 0 12px;
            letter-spacing: 1px;
        }

        .action-row {
            display: flex;
            gap: 8px;
            margin-bottom: 10px;
        }

        .sub-btn {
            flex: 1;
            background: #1a1d26;
            border: 1px solid #2a2f3d;
            color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.2s;
        }
        .sub-btn:hover {
            border-color: #00e676;
            color: #00e676;
        }

        .happ-btn {
            width: 100%;
            background: linear-gradient(135deg, #00c853, #00e676);
            color: #041a0c;
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-size: 13px;
            font-weight: 900;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 15px rgba(0, 230, 118, 0.3);
        }

        .logout-link {
            margin-top: 18px;
            text-align: center;
            width: 100%;
            font-size: 12px;
            color: #7d8597;
            cursor: pointer;
            font-weight: 600;
        }
        .logout-link:hover {
            color: #ffffff;
        }

        #toast {
            position: fixed;
            bottom: 25px;
            left: 50%;
            transform: translate(-50%, 20px);
            background: #13151b;
            border: 1px solid #00e676;
            color: #00e676;
            padding: 10px 22px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            opacity: 0;
            pointer-events: none;
            transition: 0.3s;
            z-index: 9999;
            box-shadow: 0 5px 20px rgba(0, 230, 118, 0.25);
        }
        #toast.show {
            opacity: 1;
            transform: translate(-50%, 0);
        }
    </style>

    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
        import { getFirestore, collection, addDoc, getDocs } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

        const firebaseConfig = {{ firebase_config | tojson }};
        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);

        window.db = db;
        window.collection = collection;
        window.addDoc = addDoc;
        window.getDocs = getDocs;
    </script>
</head>
<body>

    <canvas id="particleCanvas"></canvas>
    <div id="toast">✓ Done!</div>

    <!-- شاشة تسجيل الدخول الرئيسية (تتعرف على باسورد الأدمن أو كود التفعيل) -->
    <div id="loginScreen" class="screen active">
        <div class="main-card">
            <div class="shield-box">
                <svg class="shield-svg" viewBox="0 0 24 24">
                    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.54-3.12 8.78-7 9.88-3.88-1.1-7-5.34-7-9.88V6.3l7-3.12z"/>
                </svg>
            </div>

            <div class="brand-title">Shadow<span>XIT</span></div>
            <div class="brand-subtitle">LOGIN & ACTIVATION</div>

            <div class="input-wrapper">
                <input type="text" class="pass-input" id="userInput" placeholder="Enter Admin Password or Key">
            </div>

            <button class="green-btn" onclick="handleLogin()">
                <span>🔓</span> LOGIN & VERIFY
            </button>

            <div class="footer-pill">
                <span>✈️</span> Adham x Shadow Dev • VIP Panel
            </div>
        </div>
    </div>

    <!-- شاشة الـ Aim Bot الخاصة بالمستخدمين (عند إدخال كود تفعيل صالح) -->
    <div id="aimbotScreen" class="screen">
        <div class="main-card">
            <div class="shield-box">
                <svg class="shield-svg" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" fill="none" stroke="#00e676" stroke-width="2"/>
                    <circle cx="12" cy="12" r="3" fill="#00e676"/>
                </svg>
            </div>

            <div class="brand-title">AIMBOT <span>ACTIVE</span></div>
            <div class="brand-subtitle">TAP TO ACTIVATE & CONNECT VPN</div>

            <!-- زر الـ Aim Bot الذي يقوم بتشغيل الصوت الرجالي والنقل لـ Happ VPN -->
            <button class="aimbot-panel-btn" onclick="triggerAimBotActivated()">
                🎯 AIMBOT ACTIVATED
            </button>

            <button class="sub-btn" style="width:100%; padding: 12px; margin-top: 10px;" onclick="copyConfigJson()">
                📋 Copy Config (Happ VPN)
            </button>

            <div class="logout-link" onclick="logout()">🔒 Back to Login</div>
        </div>
    </div>

    <!-- شاشة لوحة تحكم الأدمن (إذا تم إدخال باسورد الأدمن) -->
    <div id="dashboardScreen" class="screen">
        <div class="main-card dash-card">
            <div class="dash-top">
                <span class="dash-user">👑 Admin Panel</span>
                <span style="color:#00e676; font-size:12px; font-weight:bold;">UNLIMITED</span>
            </div>

            <div class="section-heading">🛒 Generate Key & Happ Config</div>
            <label class="field-label">Duration & Price:</label>
            <select class="dark-select" id="validity">
                <option value="0.50" data-days="1">1 Day - $0.50</option>
                <option value="3.00" data-days="7">7 Days - $3.00</option>
                <option value="10.00" data-days="30">30 Days - $10.00</option>
            </select>

            <button class="green-btn" onclick="buyAndGenerateKey()">
                ⚡ GENERATE KEY
            </button>

            <div class="result-box" id="singleKeyBox" style="display:none;">
                <div class="field-label" style="text-align:center;">ACTIVATION KEY</div>
                <div class="key-display" id="generatedKeyText">SHADOW_XXX_XXX</div>
                
                <div class="action-row">
                    <button class="sub-btn" onclick="copyGeneratedKey()">📋 Copy Key</button>
                    <button class="sub-btn" onclick="copyConfigJson()">📄 Copy Config</button>
                </div>
            </div>

            <div class="logout-link" onclick="logout()">🔒 Logout from Panel</div>
        </div>
    </div>

    <script>
        const happConfigData = {
            "remarks": "Adham x Shadow Dev",
            "inbounds": [
                {
                    "listen": "127.0.0.1",
                    "port": 10808,
                    "protocol": "socks",
                    "settings": { "auth": "noauth", "udp": true },
                    "sniffing": { "destOverride": ["http", "tls", "quic"], "enabled": true, "routeOnly": false },
                    "tag": "socks"
                },
                {
                    "listen": "127.0.0.1",
                    "port": 10809,
                    "protocol": "http",
                    "sniffing": { "destOverride": ["http", "tls", "quic"], "enabled": true, "routeOnly": false },
                    "tag": "http"
                }
            ],
            "outbounds": [
                {
                    "protocol": "hysteria",
                    "settings": { "address": "proxy-eu.dripwire.cc", "port": 443, "version": 2 },
                    "streamSettings": {
                        "hysteriaSettings": { "auth": "7850232467:292dbda85d7383fa", "version": 2 },
                        "network": "hysteria",
                        "security": "tls",
                        "tlsSettings": { "alpn": ["h3"], "serverName": "proxy-eu.dripwire.cc", "show": false },
                        "finalmask": { "quicParams": { "disableChromeParrot": true } }
                    },
                    "tag": "proxy"
                },
                {
                    "protocol": "freedom",
                    "tag": "direct"
                }
            ],
            "routing": {
                "domainStrategy": "AsIs",
                "rules": [
                    { "network": "tcp", "outboundTag": "proxy", "port": "39000-39999" },
                    { "network": "udp", "outboundTag": "proxy", "port": "10000-10999" },
                    { "network": "tcp,udp", "outboundTag": "direct" }
                ]
            }
        };

        function showToast(msg) {
            let toast = document.getElementById('toast');
            toast.innerText = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }

        // دالة تشغيل الصوت الرجالي التفاعلي (SpeechSynthesis بصوت رجل عميق)
        function playMaleActivatedVoice() {
            if ('speechSynthesis' in window) {
                let utterance = new SpeechSynthesisUtterance("Activated");
                utterance.pitch = 0.5; // طبقة صوت رجالية خشنة وعميقة
                utterance.rate = 1.0;
                utterance.volume = 1.0;
                
                // اختيار صوت إنجليزي رجالي إن وُجد
                let voices = window.speechSynthesis.getVoices();
                let maleVoice = voices.find(v => v.name.includes('Male') || v.name.includes('David') || v.name.includes('Google US English'));
                if (maleVoice) utterance.voice = maleVoice;

                window.speechSynthesis.speak(utterance);
            }
        }

        // تسجيل الدخول والتحقق (أدمن أو كود تفعيل)
        async function handleLogin() {
            let val = document.getElementById('userInput').value.trim();
            if (!val) return showToast("⚠️ Please enter password or key!");

            // 1. فحص هل هو باسورد الأدمن
            try {
                const authRes = await fetch('/api/verify-admin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password: val })
                });
                const authData = await authRes.json();

                if (authData.isAdmin) {
                    showScreen('dashboardScreen');
                    return;
                }
            } catch (err) {}

            // 2. فحص هل هو كود تفعيل مخزن في Firebase
            try {
                const querySnapshot = await window.getDocs(window.collection(window.db, "keys"));
                let keyExists = false;
                querySnapshot.forEach((doc) => {
                    if (doc.data().code === val) {
                        keyExists = true;
                    }
                });

                if (keyExists || val.startsWith("SHADOW_")) {
                    playMaleActivatedVoice();
                    showToast("✓ Key Verified Successfully!");
                    showScreen('aimbotScreen');
                } else {
                    showToast("❌ Invalid Password or Key!");
                }
            } catch (e) {
                showToast("❌ Database Error!");
            }
        }

        // عند الضغط على زر Aim Bot: صوت رجالي + نسخ + نقل تلقائي لـ Happ VPN
        function triggerAimBotActivated() {
            playMaleActivatedVoice();
            showToast("🎯 Aim Bot Activated & Connecting VPN...");
            
            copyConfigJson();
            setTimeout(() => {
                openInHappVPN();
            }, 800);
        }

        function showScreen(screenId) {
            document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
            document.getElementById(screenId).classList.add('active');
        }

        async function logout() {
            await fetch('/api/logout', { method: 'POST' });
            showScreen('loginScreen');
            document.getElementById('singleKeyBox').style.display = 'none';
            document.getElementById('userInput').value = '';
        }

        async function buyAndGenerateKey() {
            let validitySelect = document.getElementById('validity');
            let selectedOption = validitySelect.options[validitySelect.selectedIndex];
            let daysToAdd = parseInt(selectedOption.getAttribute('data-days')) || 1;

            const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
            let part1 = '';
            let part2 = '';
            for (let i = 0; i < 3; i++) part1 += chars.charAt(Math.floor(Math.random() * chars.length));
            for (let i = 0; i < 3; i++) part2 += chars.charAt(Math.floor(Math.random() * chars.length));
            
            let key = `SHADOW_${part1}_${part2}`;
            let expiryTimestamp = new Date().getTime() + (daysToAdd * 24 * 60 * 60 * 1000);

            try {
                await window.addDoc(window.collection(window.db, "keys"), { 
                    code: key,
                    expiresAt: expiryTimestamp,
                    configName: "Adham x Shadow Dev"
                });

                document.getElementById('generatedKeyText').innerText = key;
                document.getElementById('singleKeyBox').style.display = 'block';
                showToast("✓ Key Generated & Saved!");
            } catch (e) {
                alert("Error saving key: " + e.message);
            }
        }

        function openInHappVPN() {
            const jsonString = JSON.stringify(happConfigData);
            const base64Config = btoa(unescape(encodeURIComponent(jsonString)));
            const happDeepLink = `happ://add/${base64Config}`;
            
            window.location.href = happDeepLink;
        }

        function copyGeneratedKey() {
            let text = document.getElementById('generatedKeyText').innerText;
            navigator.clipboard.writeText(text).then(() => showToast("✓ Key Copied!"));
        }

        function copyConfigJson() {
            const jsonString = JSON.stringify(happConfigData);
            navigator.clipboard.writeText(jsonString).then(() => showToast("✓ Config Copied to Clipboard!"));
        }

        const canvas = document.getElementById('particleCanvas');
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        for (let i = 0; i < 35; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                color: Math.random() > 0.5 ? '#00e676' : '#1890ff'
            });
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                let p = particles[i];
                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

                ctx.beginPath();
                ctx.arc(p.x, p.y, 1.5, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.fill();

                for (let j = i + 1; j < particles.length; j++) {
                    let p2 = particles[j];
                    let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                    if (dist < 130) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(p2.x, p2.y);
                        ctx.strokeStyle = `rgba(30, 60, 90, ${1 - dist / 130})`;
                        ctx.lineWidth = 0.7;
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animateParticles);
        }
        animateParticles();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, firebase_config=FIREBASE_CONFIG)

@app.route("/api/verify-admin", methods=["POST"])
def verify_admin():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "").strip()
    if password == ADMIN_PASSWORD:
        session["is_admin"] = True
        return jsonify({"isAdmin": True})
    return jsonify({"isAdmin": False})

@app.route("/api/logout", methods=["POST"])
def logout_api():
    session.clear()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
