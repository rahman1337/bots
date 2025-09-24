import threading
from bot import start_bot as start_bot1
from rug import start_bot as start_bot2
from flask import Flask

# Jalankan kedua bot bersamaan
threading.Thread(target=start_bot1).start()
threading.Thread(target=start_bot2).start()

# Dummy web server supaya Render mendeteksi port
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Telegram is running!"

if __name__ == "__main__":
    # Jalankan Flask di port 10000
    app.run(host="0.0.0.0", port=10000)