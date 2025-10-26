from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "🟢 Enlix Server (Render) is running!"

@app.route("/webhook/zalo", methods=["GET", "POST"])
def webhook():
    # Khi Zalo kiểm tra xác thực
    if request.method == "GET":
        verify_token = request.args.get("verify_token")
        print("🔍 Zalo đang xác thực domain:", verify_token)
        # Trả lại đúng verify_token để xác thực thành công
        return verify_token, 200

    # Khi có tin nhắn gửi đến
    elif request.method == "POST":
        data = request.json
        print("📩 Nhận được tin nhắn từ Zalo:", data)
        return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
