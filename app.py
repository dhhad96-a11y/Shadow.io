from flask import Flask, request, jsonify, session, render_template_string
import secrets

app = Flask(__name__)
# مفتاح تشفير الجلسات (يتم توليده تلقائياً لحماية دخول الأدمن)
app.secret_key = secrets.token_hex(32)

# كلمة مرور الأدمن المخفية تماماً عن كود HTML
ADMIN_PASSWORD = "ADHAM SHADOW"

# إعدادات Firebase الجديدة الخاصة بك (wbbhdh-9ede6)
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyCc-8w0G8AIxEpoScTC3eqs0rcdDWd-j8g",
    "authDomain": "wbbhdh-9ede6.firebaseapp.com",
    "projectId": "wbbhdh-9ede6",
    "storageBucket": "wbbhdh-9ede6.firebasestorage.app",
    "messagingSenderId": "426376855325",
    "appId": "1:426376855325:android:30a926985465c34d16abf4"
}

# قالب الواجهة الأمامية (خالي تماماً من كلمة مرور الأدمن)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Shadow - Reseller & Admin Access</title>
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
            fill: #ffffff;
        }

        .brand-title {
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
            color: #ffffff;
        }
        .brand-title span {
            color: #1890ff;
        }

        .brand-subtitle {
            font-size: 10px;
            font-weight: 700;
            color: #7d8597;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 26px;
        }

        .role-switcher {
            width: 100%;
            background: #0d0e12;
            border-radius: 14px;
            padding: 4px;
            display: flex;
            margin-bottom: 16px;
            border: 1px solid #1a1d26;
        }

        .role-tab {
            flex: 1;
            padding: 12px 0;
            border: none;
            border-radius: 11px;
            background: transparent;
            color: #7d8597;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.25s ease;
        }

        .role-tab.active {
            background: #00e676;
            color: #051b0e;
            box-shadow: 0 0 18px rgba(0, 230, 118, 0.45);
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

        .toggle-eye {
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            font-size: 14px;
            opacity: 0.5;
        }
        .toggle-eye:hover {
            opacity: 1;
        }

        .green-btn {
            width: 100%;
            background: #00e676;
            color: #ffffff;
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

        .balance-tag {
            background: rgba(0, 230, 118, 0.12);
            border: 1px solid rgba(0, 230, 118, 0.3);
            color: #00e676;
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 800;
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

        .reseller-box {
            width: 100%;
            max-height: 120px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 14px;
        }

        .reseller-row {
            background: #0d0e12;
            border: 1px solid #1f232d;
            padding: 10px 12px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
        }

        .del-btn {
            background: rgba(255, 59, 48, 0.15);
            border: 1px solid rgba(255, 59, 48, 0.4);
            color: #ff453a;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
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

        window.loadCloudData();
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
                    <path d="M12 3.18V20.88c3.88-1.1 7-5.34 7-9.88V6.3l-7-3.12z" opacity="0.35"/>
                </svg>
            </div>

            <div class="brand-title">Shadow<span>XIT</span></div>
            <div class="brand-subtitle" id="accessSubtitle">RESELLER ACCESS</div>

            <div class="role-switcher">
                <button type="button" class="role-tab" id="tabAdmin" onclick="selectRole('admin')">Admin</button>
                <button type="button" class="role-tab active" id="tabReseller" onclick="selectRole('reseller')">Reseller</button>
            </div>

            <div class="input-wrapper">
                <input type="password" class="pass-input" id="userInput" placeholder="Enter your password">
                <span class="toggle-eye" onclick="togglePassVisibility()">👁️</span>
            </div>

            <button class="green-btn" onclick="handleLogin()">
                <span>👤</span> LOGIN
            </button>

            <div class="footer-pill">
                <span>✈️</span> Adham x Shadow Dev • VIP Panel
            </div>
        </div>
    </div>

    <!-- شاشة لوحة التحكم -->
    <div id="dashboardScreen" class="screen">
        <div class="main-card dash-card">
            <div class="dash-top">
                <span class="dash-user" id="panelTitle">👑 Control Panel</span>
                <span class="balance-tag" id="accountBalance">UNLIMITED</span>
            </div>

            <!-- قسم إدارة الموزعين (يظهر للأدمن فقط بعد التحقق من السيرفر) -->
            <div id="adminResellerSection" style="display:none; width: 100%;">
                <div class="section-heading">👥 Manage Resellers</div>
                <label class="field-label">Reseller Password / Username:</label>
                <input type="text" class="dark-input" id="resellerName" placeholder="e.g. reseller123">
                
                <label class="field-label">Initial Balance ($):</label>
                <input type="number" class="dark-input" id="resellerBalance" value="20">
                
                <button class="green-btn" style="padding: 12px; font-size: 13px; margin-bottom: 14px;" onclick="addReseller()">
                    ➕ ADD RESELLER
                </button>

                <label class="field-label">Active Resellers:</label>
                <div class="reseller-box" id="resellerContainer"></div>
            </div>

            <!-- قسم توليد الأكواد والكونفيج -->
            <div class="section-heading">🛒 Generate Key & Happ Config</div>
            <label class="field-label">Product:</label>
            <select class="dark-select" id="productType">
                <option value="Shadow V3">Shadow v3 - Happ VPN</option>
                <option value="Shadow Client">Shadow Client - VIP</option>
            </select>

            <label class="field-label">Duration & Price:</label>
            <select class="dark-select" id="validity">
                <option value="0.50" data-days="1">1 Day - $0.50</option>
                <option value="3.00" data-days="7">7 Days - $3.00</option>
                <option value="10.00" data-days="30">30 Days - $10.00</option>
            </select>

            <button class="green-btn" onclick="buyAndGenerateKey()">
                ⚡ GENERATE KEY & CONNECT
            </button>

            <!-- صندوق النتيجة والنقل التلقائي لتطبيق Happ VPN -->
            <div class="result-box" id="singleKeyBox" style="display:none;">
                <div class="field-label" style="text-align:center;">ACTIVATION KEY</div>
                <div class="key-display" id="generatedKeyText">SHADOW_XXX_XXX</div>
                
                <div class="action-row">
                    <button class="sub-btn" onclick="copyGeneratedKey()">📋 Copy Key</button>
                    <button class="sub-btn" onclick="copyConfigJson()">📄 Copy Config</button>
                </div>

                <button class="happ-btn" onclick="openInHappVPN()">
                    🚀 نقل تلقائي إلى Happ VPN
                </button>
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

        let selectedRole = "reseller";
        let cloudResellers = [];
        let currentUserType = "reseller";
        let currentResellerId = null;
        let currentResellerData = null;

        function selectRole(role) {
            selectedRole = role;
            document.getElementById('tabAdmin').classList.toggle('active', role === 'admin');
            document.getElementById('tabReseller').classList.toggle('active', role === 'reseller');
            document.getElementById('accessSubtitle').innerText = role === 'admin' ? 'ADMIN ACCESS' : 'RESELLER ACCESS';
            document.getElementById('userInput').placeholder = role === 'admin' ? 'Enter Admin password' : 'Enter your password';
        }

        function showToast(msg) {
            let toast = document.getElementById('toast');
            toast.innerText = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }

        function togglePassVisibility() {
            let input = document.getElementById('userInput');
            input.type = input.type === "password" ? "text" : "password";
        }

        window.loadCloudData = async function() {
            try {
                const resellersSnap = await window.getDocs(window.collection(window.db, "resellers"));
                cloudResellers = resellersSnap.docs.map(d => ({ firestoreId: d.id, ...d.data() }));
            } catch (e) {
                console.error("Error loading cloud data:", e);
            }
        };

        function renderResellersUI() {
            let container = document.getElementById('resellerContainer');
            container.innerHTML = '';
            cloudResellers.forEach((r) => {
                let div = document.createElement('div');
                div.className = 'reseller-row';
                div.innerHTML = `
                    <span><b>${r.name}</b></span>
                    <div>
                        <span style="color:#00e676; font-weight:bold; margin-right:10px;">$${Number(r.balance).toFixed(2)}</span>
                        <button class="del-btn" onclick="deleteResellerCloud('${r.firestoreId}')">Delete</button>
                    </div>
                `;
                container.appendChild(div);
            });
        }

        // التحقق من باسورد الأدمن يتم عبر السيرفر (Python) ولا يوجد في HTML
        window.handleLogin = async function() {
            let val = document.getElementById('userInput').value.trim();
            if (!val) return showToast("⚠️ Please enter your password!");

            // إرسال الطلب إلى Python للتحقق من باسورد الأدمن بأمان
            try {
                const authRes = await fetch('/api/verify-admin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password: val })
                });
                const authData = await authRes.json();

                if (authData.isAdmin) {
                    await window.loadCloudData();
                    currentUserType = "admin";
                    document.getElementById('panelTitle').innerText = "👑 Admin Control";
                    document.getElementById('accountBalance').innerText = "UNLIMITED";
                    document.getElementById('adminResellerSection').style.display = 'block';
                    showDashboard();
                    return;
                }
            } catch (err) {
                console.error("Auth check error:", err);
            }

            if (selectedRole === "admin") {
                showToast("❌ Invalid Admin Password!");
                return;
            }

            // التحقق من حساب الموزع في Firebase
            await window.loadCloudData();
            let found = cloudResellers.find(r => r.name.toLowerCase() === val.toLowerCase());
            if (found) {
                currentUserType = "reseller";
                currentResellerId = found.firestoreId;
                currentResellerData = found;
                document.getElementById('panelTitle').innerText = `👤 ${found.name}`;
                document.getElementById('accountBalance').innerText = `$${Number(found.balance).toFixed(2)}`;
                document.getElementById('adminResellerSection').style.display = 'none';
                showDashboard();
            } else {
                showToast("❌ Invalid Password!");
            }
        };

        function showDashboard() {
            document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
            document.getElementById('dashboardScreen').classList.add('active');
            renderResellersUI();
        }

        async function logout() {
            await fetch('/api/logout', { method: 'POST' });
            document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
            document.getElementById('loginScreen').classList.add('active');
            document.getElementById('singleKeyBox').style.display = 'none';
            document.getElementById('userInput').value = '';
        }

        window.addReseller = async function() {
            let name = document.getElementById('resellerName').value.trim();
            let balance = parseFloat(document.getElementById('resellerBalance').value);

            if (!name) return showToast('⚠️ Enter reseller password/name');
            if (cloudResellers.some(r => r.name.toLowerCase() === name.toLowerCase())) {
                return showToast('⚠️ Reseller already exists!');
            }

            try {
                const docRef = await window.addDoc(window.collection(window.db, "resellers"), {
                    name: name,
                    balance: balance || 0
                });
                cloudResellers.push({ firestoreId: docRef.id, name: name, balance: balance || 0 });
                renderResellersUI();
                document.getElementById('resellerName').value = '';
                showToast(`✓ Reseller ${name} Added!`);
            } catch (e) {
                alert("Firebase Error: " + e.message);
            }
        };

        window.deleteResellerCloud = async function(firestoreId) {
            if (confirm("Delete this reseller?")) {
                try {
                    await window.deleteDoc(window.doc(window.db, "resellers", firestoreId));
                    cloudResellers = cloudResellers.filter(r => r.firestoreId !== firestoreId);
                    renderResellersUI();
                    showToast("✓ Reseller Deleted!");
                } catch (e) {
                    alert("Error deleting: " + e.message);
                }
            }
        };

        window.buyAndGenerateKey = async function() {
            let priceSelect = document.getElementById('validity');
            let price = parseFloat(priceSelect.value);
            let selectedOption = priceSelect.options[priceSelect.selectedIndex];
            let daysToAdd = parseInt(selectedOption.getAttribute('data-days')) || 1;

            if (currentUserType === "reseller") {
                if (currentResellerData.balance < price) {
                    return showToast("❌ Insufficient Balance!");
                }
                currentResellerData.balance -= price;
                
                try {
                    await window.updateDoc(window.doc(window.db, "resellers", currentResellerId), {
                        balance: currentResellerData.balance
                    });
                    document.getElementById('accountBalance').innerText = `$${Number(currentResellerData.balance).toFixed(2)}`;
                } catch (e) {
                    return alert("Error updating balance: " + e.message);
                }
            }

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
                showToast("✓ Key Generated! Opening Happ VPN...");

                setTimeout(() => {
                    openInHappVPN();
                }, 800);

            } catch (e) {
                alert("Error saving key: " + e.message);
            }
        };

        function openInHappVPN() {
            const jsonString = JSON.stringify(happConfigData);
            const base64Config = btoa(unescape(encodeURIComponent(jsonString)));
            const happDeepLink = `happ://add/${base64Config}`;
            
            navigator.clipboard.writeText(jsonString).catch(() => {});
            window.location.href = happDeepLink;
        }

        function copyGeneratedKey() {
            let text = document.getElementById('generatedKeyText').innerText;
            navigator.clipboard.writeText(text).then(() => showToast("✓ Key Copied!"));
        }

        function copyConfigJson() {
            const jsonString = JSON.stringify(happConfigData);
            navigator.clipboard.writeText(jsonString).then(() => showToast("✓ Config Copied!"));
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
