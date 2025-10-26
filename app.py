from flask import Flask, request, send_from_directory
import os, requests

app = Flask(__name__)

# 🧠 OA Access Token của bạn (thay bằng token thật)
ACCESS_TOKEN = "6uTm6yyMQZyNZt8Pm1PhFnQ4THx22YfQGSurDl0XAMXcstuTo0qoRndYMIck6o498unVLVTs22b2kczjbsa6DGM8N6YqVXnAORzb7-X977rjl65RpqWk96QTD5MsKIuo3fPQQeLC54a1gd8bZ70EHoUAS6VpOoqBQx4nQF1WLJbcjWnslsD446VsEdEr7Y5KBFPA6ACq0ICZn1jZzWu0BIJCNbQTNYGp5h5PTxfYCLGIyqnsdJWGM0RgQIQD0Gzv9iX53lSBCMX_t5uyxXf1S6I2BIJaL6jnSiqB4FbLKaXMk0Osv6X2K7668XFLG6nH1Byl8ObyH6u4v1WVW1SOO2ldOW6wFnOWAF59OvDZCmCmW2rZX6PZ3J2t9q-LPs1qCO0W685DOsCNZsCNW7ztRG-y24giKMi6HpZXe2qMpWbiFm"

@app.route("/<path:filename>")
def serve_static(filename):
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    return "File not found", 404

@app.route("/")
def home():
    return "🟢 Enlix Server is running and connected to Zalo OA!"

@app.route("/webhook/zalo", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("verify_token")
        return verify_token, 200

    elif request.method == "POST":
        data = request.json
        print("📩 Nhận tin nhắn từ Zalo:", data)

        # Kiểm tra có tin nhắn văn bản không
        try:
            user_id = data["message"]["user_id"]
            text = data["message"]["text"]

            # ✅ Trả lời lại người dùng
            reply_text = f"Bạn vừa nhắn: {text}\nEnlix nhận được rồi 🚀"

            send_zalo_message(user_id, reply_text)
        except Exception as e:
            print("❌ Lỗi xử lý:", e)

        return {"ok": True}, 200

def send_zalo_message(user_id, text):
    """Gửi tin nhắn Zalo OA"""
    url = "https://openapi.zalo.me/v2.0/oa/message"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    payload = {
        "recipient": {"user_id": user_id},
        "message": {"text": text}
    }
    res = requests.post(url, headers=headers, json=payload)
    print("📤 Gửi tin nhắn:", res.text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
