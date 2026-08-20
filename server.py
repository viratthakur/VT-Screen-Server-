# Copyright (c) 2026 VIRAT THAKUR. All Rights Reserved.
# Original Author: VIRAT THAKUR (YouTube: @VIRATH4K3R)
# Unauthorized copying, modification, or redistribution is prohibited.
# This code was created for educational/portfolio purposes only.--

from flask import Flask, Response, render_template_string
import mss
from PIL import Image
import io
import threading
import socket

app = Flask(__name__)
lock = threading.Lock()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Screen Share</title>
    <style>
        body { margin:0; background:#000; display:flex;
               justify-content:center; align-items:center; height:100vh; }
        img  { max-width:100%; max-height:100vh; }
    </style>
</head>
<body>
    <img src="/stream" />
</body>
</html>
"""

def vt_capture_screen():
    with lock:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=60)
            buf.seek(0)
            return buf.read()

def generate_frames():
    while True:
        frame = vt_capture_screen()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/stream")
def stream():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

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
    ip = vt_get_my_ip()
    port = 5050
    print("\n" + "="*55)
    print("  VT-Screen-Server")
    print("  Original Author :- VIRAT THAKUR")
    print("  YouTube Channel : @VIRATH4K3R")
    print("  https://www.youtube.com/@VIRATH4K3R")
    print(f"\n[*] Screen Share Server chalu hai boss man")
    print(f"[*] Local URL: http://{ip}:{port}")
    print(f"[*] Band karne ke liye: Ctrl+C\n")
    app.run(host="0.0.0.0", port=5050, threaded=True)
