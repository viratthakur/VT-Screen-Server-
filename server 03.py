# Copyright (c) 2026 VIRAT THAKUR. All Rights Reserved.
# Original Author: VIRAT THAKUR (YouTube: @VIRATH4K3R)
# Unauthorized copying, modification, or redistribution is prohibited.
# This code was created for educational/portfolio purposes only.

print(f"\n[*] Screen Share Server chalu hai boss man")  # yeh aapka signature hai
# ============================================================
# VT-Screen-Server
# Original Author : VIRAT THAKUR
# YouTube         : @VIRATH4K3R
# Created         : 2026
# ============================================================
# This code is proprietary. 
# Do not copy, rewrite with AI, or claim as your own work.
# ============================================================

from flask import Flask, render_template_string, Response, request
from flask_sock import Sock
import mss
from PIL import Image
import io
import socket
import time

app = Flask(__name__)
sock = Sock(app)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Screen Share</title>
    <style>
        * { margin:0; padding:0; }
        body { background:#000; display:flex;
               justify-content:center; align-items:center; height:100vh; }
        canvas { max-width:100%; max-height:100vh; }
        #status { position:fixed; top:10px; left:10px; 
                  color:#0f0; font-family:monospace; font-size:12px; }
    </style>
</head>
<body>
    <div id="status">Connecting...</div>
    <canvas id="screen"></canvas>
    <script>
        const canvas = document.getElementById('screen');
        const ctx = canvas.getContext('2d');
        const status = document.getElementById('status');

        // Auto detect ws ya wss
        const protocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
        const ws = new WebSocket(protocol + location.host + '/ws');
        ws.binaryType = 'blob';

        let rendering = false;

        ws.onopen = () => status.textContent = 'Connected';
        ws.onclose = () => {
            status.textContent = 'Disconnected - Reconnecting...';
            setTimeout(() => location.reload(), 2000);
        };
        ws.onerror = () => {
            status.textContent = 'Error - Reconnecting...';
            setTimeout(() => location.reload(), 2000);
        };

        ws.onmessage = function(event) {
            if (rendering) return;
            rendering = true;
            const url = URL.createObjectURL(event.data);
            const img = new Image();
            img.onload = () => {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                URL.revokeObjectURL(url);
                rendering = false;
            };
            img.src = url;
        };
    </script>
</body>
</html>
"""

def vt_capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img = img.resize((960, 540), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=50)
        buf.seek(0)
        return buf.read()

@app.route("/")
def index():
    return render_template_string(HTML)

@sock.route("/ws")
def stream(ws):
    while True:
        try:
            start = time.time()
            frame = vt_capture_screen()
            ws.send(frame)
            elapsed = time.time() - start
            time.sleep(max(0, 0.05 - elapsed))
        except Exception:
            break

def vt_get_my_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    ip =vt_get_my_ip()
    port = 5050
    print("\n" + "="*55)
    print("  VT-Screen-Server")
    print("  Original Author : VIRAT THAKUR")
    print("  YouTube Channel : @VIRATH4K3R")
    print("  https://www.youtube.com/@VIRATH4K3R")
    print(f"\n[*] Screen Share Server chalu hai boss man")
    print(f"[*] Local URL:  http://{ip}:{port}")
    print(f"[*] Ngrok URL:  https://antihero-certainly-aftermost.ngrok-free.dev")
    print(f"[*] Band karne ke liye: Ctrl+C\n")
    app.run(host="0.0.0.0", port=5050, threaded=True)
