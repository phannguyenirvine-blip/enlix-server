from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# Cho phép truy cập file HTML xác minh
@app.route("/<path:filename>")
def serve_static(filename):
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    return "File not found", 404

@app.route("/")
def home():
    return "🟢 Enlix Server (Render) is running!"

@app.route("/webhook/zalo", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("verify_token")
        print("🔍 Xác thực domain từ Zalo:", verify_token)
        return verify_token, 200
    elif request.method == "POST":
        data = request.json
        print("📩 Nhận được tin nhắn từ Zalo:", data)
        return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
