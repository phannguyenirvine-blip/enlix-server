from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "🟢 Enlix Server (Render) is running!"

# ✅ Webhook có xác thực domain + nhận dữ liệu tin nhắn
@app.route("/webhook/zalo", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Zalo gửi verify_token để kiểm tra
        token = request.args.get("verify_token")
        print(f"🔍 Xác thực domain từ Zalo: {token}")
        return token  # Zalo cần server trả lại y hệt token này
    elif request.method == "POST":
        data = request.json
        print("📩 Nhận được tin nhắn từ Zalo:", data)
        return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
