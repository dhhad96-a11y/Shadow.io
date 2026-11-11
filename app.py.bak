from flask import Flask, request, jsonify, session, render_template_string
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

ADMIN_PASSWORD = "ADHAM SHADOW"

# إعدادات Firebase المحدثة بدقة
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
    <title>Shadow - Admin & Reseller Panel</title>
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
            max-width: 420px;
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
            padding: 30px 20px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75);
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .shield-box {
            width: 60px;
            height: 60px;
            background: linear-gradient(145deg, #1d2230, #161923);
            border: 1px solid #292f42;
            border-radius: 16px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 15px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        }

        .shield-svg {
            width: 30px;
            height: 30px;
            fill: #00e676;
        }

        .brand-title {
            font-size: 24px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
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
            margin-bottom: 20px;
        }

        .input-wrapper {
            width: 100%;
            position: relative;
            margin-bottom: 14px;
        }

        .pass-input {
            width: 100%;
            background: #0d0e12;
            border: 1px solid #1a1d26;
            border-radius: 14px;
            padding: 14px 18px;
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
            padding: 14px;
            font-size: 13px;
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
        }

        .aimbot-panel-btn {
            width: 100%;
            background: linear-gradient(135deg, #ff3b30, #ff9500);
            color: #ffffff;
            border: none;
            border-radius: 14px;
            padding: 16px;
            font-size: 15px;
            font-weight: 900;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-bottom: 14px;
            box-shadow: 0 8px 25px rgba(255, 59, 48, 0.4);
        }

        .footer-pill {
            margin-top: 18px;
            background: rgba(0, 230, 118, 0.08);
            border: 1px solid rgba(0, 230, 118, 0.22);
            border-radius: 999px;
            padding: 6px 16px;
            font-size: 10px;
            font-weight: 700;
            color: #00e676;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .dash-card {
            padding: 20px;
            text-align: left;
            max-height: 92vh;
            overflow-y: auto;
        }

        .dash-top {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 12px;
            margin-bottom: 14px;
            border-bottom: 1px solid #1f232d;
        }

        .dash-user {
            font-size: 13px;
            font-weight: 800;
            color: #ffffff;
        }

        .section-heading {
            width: 100%;
            font-size: 11px;
            font-weight: 800;
            color: #00e676;
            margin: 12px 0 6px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .field-label {
            width: 100%;
            font-size: 10px;
            color: #7d8597;
            margin-bottom: 4px;
            font-weight: 600;
        }

        .dark-input, .dark-select {
            width: 100%;
            background: #0d0e12;
            border: 1px solid #1f232d;
            border-radius: 10px;
            padding: 10px 12px;
            color: #ffffff;
            font-size: 12px;
            margin-bottom: 10px;
            outline: none;
        }
        .dark-input:focus, .dark-select:focus {
            border-color: #00e676;
        }

        .list-container {
            width: 100%;
            max-height: 140px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 10px;
        }

        .list-row {
            background: #0d0e12;
            border: 1px solid #1f232d;
            padding: 8px 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
        }

        .action-btn-danger {
            background: rgba(255, 59, 48, 0.15);
            border: 1px solid rgba(255, 59, 48, 0.4);
            color: #ff453a;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 700;
            cursor: pointer;
        }

        .action-btn-warn {
            background: rgba(255, 149, 0, 0.15);
            border: 1px solid rgba(255, 149, 0, 0.4);
            color: #ff9500;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 700;
            cursor: pointer;
        }

        .action-btn-success {
            background: rgba(0, 230, 118, 0.15);
            border: 1px solid rgba(0, 230, 118, 0.4);
            color: #00e676;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 700;
            cursor: pointer;
        }

        .result-box {
            width: 100%;
            background: #0d0e12;
            border: 1px dashed #00e676;
            border-radius: 12px;
            padding: 14px;
            margin-top: 14px;
            text-align: center;
        }

        .key-display {
            font-family: monospace;
            font-size: 14px;
            font-weight: 800;
            color: #00e676;
            margin: 6px 0 10px;
            letter-spacing: 1px;
        }

        .sub-btn {
            flex: 1;
            background: #1a1d26;
            border: 1px solid #2a2f3d;
            color: #ffffff;
            padding: 8px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
        }
        .sub-btn:hover {
            border-color: #00e676;
            color: #00e676;
        }

        .logout-link {
            margin-top: 14px;
            text-align: center;
            width: 100%;
            font-size: 11px;
            color: #7d8597;
            cursor: pointer;
            font-weight: 600;
        }
        .logout-link:hover {
            color: #ffffff;
        }

        #toast {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translate(-50%, 20px);
            background: #13151b;
            border: 1px solid #00e676;
            color: #00e676;
            padding: 8px 18px;
            border-radius: 999px;
            font-size: 11px;
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
        import { getFirestore, collection, addDoc, getDocs, deleteDoc, doc, updateDoc } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

        const firebaseConfig = {{ firebase_config | tojson }};
        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);

        window.db = db;
        window.collection = collection;
        window.addDoc = addDoc;
        window.getDocs = getDocs;
        window.deleteDoc = deleteDoc;
        window.doc = doc;
        window.updateDoc = updateDoc;
    </script>
</head>
<body>

    <canvas id="particleCanvas"></canvas>
    <div id="toast">✓ Done!</div>

    <!-- شاشة تسجيل الدخول -->
    <div id="loginScreen" class="screen active">
        <div class="main-card">
            <div class="shield-box">
                <svg class="shield-svg" viewBox="0 0 24 24">
                    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.54-3.12 8.78-7 9.88-3.88-1.1-7-5.34-7-9.88V6.3l7-3.12z"/>
                </svg>
            </div>

            <div class="brand-title">Adham<span>Dev</span></div>
            <div class="brand-subtitle">ADMIN / RESELLER / KEY LOGIN</div>

            <div class="input-wrapper">
                <input type="text" class="pass-input" id="userInput" placeholder="Enter Admin Pass, Reseller Name, or Key">
            </div>

            <button class="green-btn" onclick="handleLogin()">
                <span>🔓</span> LOGIN TO SYSTEM
            </button>

            <div class="footer-pill">
                <span>✈️</span> Adham Dev • VIP Panel
            </div>
        </div>
    </div>

    <!-- شاشة الـ Aim Bot للمستخدمين -->
    <div id="aimbotScreen" class="screen">
        <div class="main-card">
            <div class="shield-box">
                <svg class="shield-svg" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" fill="none" stroke="#00e676" stroke-width="2"/>
                    <circle cx="12" cy="12" r="3" fill="#00e676"/>
                </svg>
            </div>

            <div class="brand-title">AIMBOT <span>ACTIVE</span></div>
            <div class="brand-subtitle" id="userRoleSubtitle">VIP USER PANEL</div>

            <button class="aimbot-panel-btn" onclick="triggerAimBotActivated()">
                🎯 AIMBOT ACTIVATED
            </button>

            <button class="sub-btn" style="width:100%; padding: 12px; margin-top: 6px;" onclick="fetchAndConnectVPN()">
                🚀 Connect VPN Directly
            </button>

            <div class="logout-link" onclick="logout()">🔒 Logout</div>
        </div>
    </div>

    <!-- لوحة تحكم الأدمن -->
    <div id="dashboardScreen" class="screen">
        <div class="main-card dash-card">
            <div class="dash-top">
                <span class="dash-user" id="panelHeaderTitle">👑 Adham Dev Master Panel</span>
                <span style="color:#00e676; font-size:11px; font-weight:bold;">UNLIMITED</span>
            </div>

            <div class="section-heading">👥 Manage Resellers (البائعين)</div>
            <label class="field-label">Reseller Username / Password:</label>
            <input type="text" class="dark-input" id="resellerUsername" placeholder="e.g. reseller_ahmed">
            <label class="field-label">Initial Balance ($):</label>
            <input type="number" class="dark-input" id="resellerBalance" value="20">
            <button class="green-btn" style="padding: 10px; font-size: 12px; margin-bottom: 10px;" onclick="addReseller()">
                ➕ Add Reseller Account
            </button>
            <label class="field-label">Active Resellers List:</label>
            <div class="list-container" id="resellersContainer"></div>

            <div class="section-heading">🛒 Generate & Manage Keys (إدارة الأكواد)</div>
            <label class="field-label">Duration & Validity (مدة الكود):</label>
            <select class="dark-select" id="validity">
                <option value="0.50" data-days="1">1 Day - $0.50</option>
                <option value="3.00" data-days="7">7 Days - $3.00</option>
                <option value="10.00" data-days="30">30 Days - $10.00</option>
            </select>
            <button class="green-btn" onclick="buyAndGenerateKey()">
                ⚡ GENERATE NEW KEY
            </button>

            <div class="result-box" id="singleKeyBox" style="display:none;">
                <div class="field-label" style="text-align:center;">GENERATED KEY</div>
                <div class="key-display" id="generatedKeyText">SHADOW_XXX_XXX</div>
                <div style="display: flex; gap: 6px;">
                    <button class="sub-btn" onclick="copyGeneratedKey()">📋 Copy Key</button>
                    <button class="sub-btn" onclick="fetchAndConnectVPN()">🚀 Connect VPN</button>
                </div>
            </div>

            <label class="field-label" style="margin-top: 14px;">All Generated Keys & Control (التحكم بالأكواد):</label>
            <div class="list-container" id="keysContainer" style="max-height: 160px;"></div>

            <div class="logout-link" onclick="logout()">🔒 Logout from Admin Panel</div>
        </div>
    </div>

    <script>
        const configUrl = "https://github.com/Dev0x1exe/deev/raw/refs/heads/main/aimbot.json";

        function showToast(msg) {
            let toast = document.getElementById('toast');
            toast.innerText = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }

        function playMaleActivatedVoice() {
            if ('speechSynthesis' in window) {
                let utterance = new SpeechSynthesisUtterance("Activated");
                utterance.pitch = 0.5;
                utterance.rate = 1.0;
                utterance.volume = 1.0;
                window.speechSynthesis.speak(utterance);
            }
        }

        async function handleLogin() {
            let val = document.getElementById('userInput').value.trim();
            if (!val) return showToast("⚠️ Please enter password or key!");

            try {
                const authRes = await fetch('/api/verify-admin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password: val })
                });
                const authData = await authRes.json();
                if (authData.isAdmin) {
                    loadAdminData();
                    showScreen('dashboardScreen');
                    return;
                }
            } catch (err) {}

            try {
                const resellersSnap = await window.getDocs(window.collection(window.db, "resellers"));
                let foundReseller = null;
                resellersSnap.forEach((docSnap) => {
                    if (docSnap.data().name.toLowerCase() === val.toLowerCase()) {
                        foundReseller = docSnap.data();
                    }
                });

                if (foundReseller) {
                    document.getElementById('userRoleSubtitle').innerText = `RESELLER: ${foundReseller.name} ($${foundReseller.balance})`;
                    showScreen('aimbotScreen');
                    return;
                }

                const keysSnap = await window.getDocs(window.collection(window.db, "keys"));
                let validKey = null;
                keysSnap.forEach((docSnap) => {
                    let kData = docSnap.data();
                    if (kData.code === val && kData.active !== false) {
                        validKey = kData;
                    }
                });

                if (validKey) {
                    playMaleActivatedVoice();
                    document.getElementById('userRoleSubtitle').innerText = `KEY USER (Created by: ${validKey.createdBy || 'Admin'})`;
                    showScreen('aimbotScreen');
                } else {
                    showToast("❌ Invalid Password, Reseller, or Disabled Key!");
                }
            } catch (e) {
                showToast("❌ Database Error!");
            }
        }

        async function loadAdminData() {
            const resellersContainer = document.getElementById('resellersContainer');
            resellersContainer.innerHTML = 'Loading...';
            try {
                const resellersSnap = await window.getDocs(window.collection(window.db, "resellers"));
                resellersContainer.innerHTML = '';
                resellersSnap.forEach((docSnap) => {
                    let r = docSnap.data();
                    let div = document.createElement('div');
                    div.className = 'list-row';
                    div.innerHTML = `
                        <span><b>${r.name}</b> ($${r.balance})</span>
                        <button class="action-btn-danger" onclick="deleteReseller('${docSnap.id}')">Delete</button>
                    `;
                    resellersContainer.appendChild(div);
                });
            } catch (e) { resellersContainer.innerHTML = 'Error loading'; }

            const keysContainer = document.getElementById('keysContainer');
            keysContainer.innerHTML = 'Loading...';
            try {
                const keysSnap = await window.getDocs(window.collection(window.db, "keys"));
                keysContainer.innerHTML = '';
                keysSnap.forEach((docSnap) => {
                    let k = docSnap.data();
                    let isActive = k.active !== false;
                    let div = document.createElement('div');
                    div.className = 'list-row';
                    div.innerHTML = `
                        <div style="font-family:monospace; font-size:10px;">
                            <b>${k.code}</b><br>
                            <span style="color:#7d8597;">By: ${k.createdBy || 'Admin'} | ${k.duration || '1 Day'}</span>
                        </div>
                        <div style="display:flex; gap:4px;">
                            <button class="${isActive ? 'action-btn-warn' : 'action-btn-success'}" onclick="toggleKeyStatus('${docSnap.id}', ${isActive})">
                                ${isActive ? 'Disable' : 'Enable'}
                            </button>
                            <button class="action-btn-danger" onclick="deleteKey('${docSnap.id}')">Del</button>
                        </div>
                    `;
                    keysContainer.appendChild(div);
                });
            } catch (e) { keysContainer.innerHTML = 'Error loading keys'; }
        }

        async function addReseller() {
            let name = document.getElementById('resellerUsername').value.trim();
            let balance = parseFloat(document.getElementById('resellerBalance').value) || 0;
            if (!name) return showToast("⚠️ Enter reseller name!");

            try {
                await window.addDoc(window.collection(window.db, "resellers"), { name, balance });
                document.getElementById('resellerUsername').value = '';
                showToast("✓ Reseller Added Successfully!");
                loadAdminData();
            } catch (e) { alert("Error: " + e.message); }
        }

        async function deleteReseller(id) {
            if (confirm("Delete this reseller?")) {
                await window.deleteDoc(window.doc(window.db, "resellers", id));
                showToast("✓ Reseller Deleted!");
                loadAdminData();
            }
        }

        async function buyAndGenerateKey() {
            let validitySelect = document.getElementById('validity');
            let selectedOption = validitySelect.options[validitySelect.selectedIndex];
            let durationText = selectedOption.text;
            let daysToAdd = parseInt(selectedOption.getAttribute('data-days')) || 1;

            const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
            let part1 = '', part2 = '';
            for (let i = 0; i < 3; i++) part1 += chars.charAt(Math.floor(Math.random() * chars.length));
            for (let i = 0; i < 3; i++) part2 += chars.charAt(Math.floor(Math.random() * chars.length));
            
            let key = `SHADOW_${part1}_${part2}`;
            let expiryTimestamp = new Date().getTime() + (daysToAdd * 24 * 60 * 60 * 1000);

            try {
                await window.addDoc(window.collection(window.db, "keys"), { 
                    code: key,
                    expiresAt: expiryTimestamp,
                    duration: durationText,
                    createdBy: "Admin",
                    active: true
                });

                document.getElementById('generatedKeyText').innerText = key;
                document.getElementById('singleKeyBox').style.display = 'block';
                showToast("✓ Key Generated & Saved!");
                loadAdminData();
            } catch (e) { alert("Error: " + e.message); }
        }

        async function toggleKeyStatus(id, currentStatus) {
            try {
                await window.updateDoc(window.doc(window.db, "keys", id), { active: !currentStatus });
                showToast("✓ Key status updated!");
                loadAdminData();
            } catch (e) { alert("Error: " + e.message); }
        }

        async function deleteKey(id) {
            if (confirm("Delete this key?")) {
                await window.deleteDoc(window.doc(window.db, "keys", id));
                showToast("✓ Key Deleted!");
                loadAdminData();
            }
        }

        async function fetchAndConnectVPN() {
            try {
                showToast("⏳ Fetching Adham Dev Config...");
                const response = await fetch(configUrl);
                const configJson = await response.json();
                
                configJson.remarks = "Adham Dev";

                const jsonString = JSON.stringify(configJson);
                const base64Config = btoa(unescape(encodeURIComponent(jsonString)));
                
                showToast("✓ Opening Happ VPN...");
                
                setTimeout(() => {
                    window.location.href = `happ://add/${base64Config}`;
                }, 600);
            } catch (err) {
                showToast("❌ Failed to fetch config from URL!");
            }
        }

        function triggerAimBotActivated() {
            playMaleActivatedVoice();
            showToast("🎯 Aim Bot Activated & Connecting VPN...");
            fetchAndConnectVPN();
        }

        function copyGeneratedKey() {
            let text = document.getElementById('generatedKeyText').innerText;
            navigator.clipboard.writeText(text).then(() => showToast("✓ Key Copied!"));
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

        const canvas = document.getElementById('particleCanvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        for (let i = 0; i < 35; i++) {
            particles.push({
                x: Math.random() * canvas.width, y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.4, vy: (Math.random() - 0.5) * 0.4,
                color: Math.random() > 0.5 ? '#00e676' : '#1890ff'
            });
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
                ctx.beginPath(); ctx.arc(p.x, p.y, 1.5, 0, Math.PI * 2);
                ctx.fillStyle = p.color; ctx.fill();
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
