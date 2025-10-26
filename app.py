from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "🟢 Enlix Server (Render) is running!"

@app.route("/webhook/zalo", methods=["POST"])
def webhook():
    data = request.json
    print("📩 Nhận được tin nhắn từ Zalo:", data)
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
