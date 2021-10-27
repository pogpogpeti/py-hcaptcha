from ..utils import is_main_process
import multiprocessing
import os
import random
import subprocess
import threading
import ctypes
import time

latest_data = multiprocessing.Value(ctypes.c_wchar_p, "")
latest_proof = multiprocessing.Value(ctypes.c_wchar_p, "")
data_event = multiprocessing.Event()
proof_set_event = multiprocessing.Event()

if is_main_process():
    from flask import Flask
    from flask_socketio import SocketIO

    app = Flask(__name__)
    sio_server = SocketIO(app)
    proof_event = threading.Event()

    @sio_server.on("response")
    def response_passer(token):
        latest_proof.value = token
        proof_event.set()

    @app.route("/")
    def index_view():
        with open("hcaptcha-js/hsw.js") as fp:
            code = fp.read()
        
        return """
        <html>
        <head></head>
        <body>
            <h1>OK</h1>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
            <script>""" + code +"""</script>
            <script type="text/javascript" charset="utf-8">
                var socket = io()

                socket.on('connect', async function() {
                    setTimeout(() => location.reload(), 10000)
                })

                socket.on('request', async function(data) {
                    let token = await hsw(data)
                    socket.emit('response', token)
                })
            </script>
        </body>
        </html>
        """
        
    threading.Thread(
        target=sio_server.run,
        daemon=True,
        args=(app,),
        kwargs={"port": 9932}
        ).start()

    if os.name == "nt":
        subprocess.call(["taskkill", "/f", "/im", "chrome.exe"])
        browser = subprocess.Popen([
            os.environ["PROGRAMFILES"] + "/Google/Chrome/Application/chrome.exe",
            "--start-maximized",
            "--disable-gpu",
            "--new-window",
            "-incognito",
            "http://localhost:9932/"])
    
    else:
        subprocess.call(["pkill", "-9", "chrome"])
        browser = subprocess.Popen([
            "google-chrome",
            "--start-maximized",
            "--disable-gpu",
            "--new-window",
            "-incognito",
            "http://localhost:9932/"])

    def proof_updater():
        while True:
            try:
                data_event.wait()
                data_event.clear()
                sio_server.emit("request", latest_data.value)
                if not proof_event.wait(timeout=5):
                    continue
                proof_event.clear()
                proof_set_event.set()
            except:
                pass

    threading.Thread(target=proof_updater).start()
    time.sleep(5)
            
def get_proof(data):
    latest_data.value = data
    data_event.set()
    proof_set_event.wait()
    proof = latest_proof.value + "".join(random.choices("ghijklmnopqrstuvwxyz", k=5))
    return proof