<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="theme-color" content="#0A0A0A">
<title>Client Wire</title>
<style>
html,body{height:100%;margin:0;background:#0A0A0A;color:#2196F3;display:flex;align-items:center;justify-content:center;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
.box{text-align:center}.spinner{width:44px;height:44px;border:4px solid rgba(33,150,243,.2);border-top-color:#2196F3;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 16px}
@keyframes spin{to{transform:rotate(360deg)}}.txt{font-size:.8rem;font-weight:900;letter-spacing:2px;color:#2196F3}
</style>
</head>
<body>
<div class="box"><div class="spinner"></div><div class="txt">CLIENT WIRE · LOADING...</div></div>
<script>
var VERSION = '1.0';
location.replace('app-v' + VERSION + '.html');
</script>
</body>
</html>
