from flask import Flask, request
import os, json, threading, requests

app = Flask(__name__)

# ⚙️ Dán OA Access Token vào đây (từ API Explorer)
ACCESS_TOKEN = "9V4HPgo5Pnif-HDaeuLc6oZo56EXcMrSQeuOVxclE6aqfYfsxRG00NotSJtra6X52xzpRUUk0XTfeGzXkTqc6a7XDJsram8QExjq3CEXKWGvZNHol9TcIMVcTMEeq6rXOiqPOU-b0Nmmj1K2zfitUWlj8MU6mIfATyPVKOx0VLHvndH-ZhP0HrcdE46XlHjjLzK5TfhX3d9HuWXfkvKy43EnEXwseXPeOQuPVegIEL1UuY9fW-5IQqVYM5ojqtqYVCbeLV7QJriwrLfbvE5yMGcH3KRnkW4aFRfuBl36L18ByMqgrl5FLGNJNsh_zrTG1FL6VD_0Q6mdj7mItRTiQGABR17vbXKS9w0UF-hT4aKltZXenDPKIHhzH3R2wpD94PyzCUgAAZzkcpqIixr4R7hFGNMfqcLAJxn5GK-jcc4R"

def send_zalo_message(user_id, text):
    """Gửi tin nhắn phản hồi đến người dùng"""
    url = "https://openapi.zalo.me/v2.0/oa/message"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    payload = {
        "recipient": {"user_id": user_id},
        "message": {"text": text}
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        print("\n📤 Phản hồi gửi đến Zalo:")
        print(res.text)
    except Exception as e:
        print(f"❌ Lỗi khi gửi tin nhắn: {e}")

def process_webhook(data):
    """Xử lý webhook song song, tránh timeout"""
    print("\n🔍 WEBHOOK DEBUG — DỮ LIỆU NHẬN ĐƯỢC TỪ ZALO:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    try:
        event = data.get("event_name")
        if event == "user_send_text":
            user_id = data["message"]["user_id"]
            text = data["message"]["text"]
            reply = f"Enlix đã nhận được tin của bạn: {text}"
            send_zalo_message(user_id, reply)
        else:
            print(f"⚙️ Nhận event khác: {event}")
    except Exception as e:
        print(f"❌ Lỗi xử lý webhook: {e}")

@app.route("/")
def home():
    return "🟢 EnlixS đang hoạt động và kết nối với Zalo OA!"

@app.route("/webhook/zalo", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return request.args.get("verify_token", "OK"), 200

    # --- In ra toàn bộ dữ liệu Zalo gửi ---
    print("\n🧾 RAW WEBHOOK PAYLOAD:")
    print(request.data.decode("utf-8"))  # In nguyên văn nội dung body

    # --- Thử parse JSON nếu có ---
    try:
        data = request.get_json(force=True)
        print("\n✅ PARSED JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Không parse được JSON: {e}")
        data = {}

    # --- Gọi hàm xử lý ---
    threading.Thread(target=process_webhook, args=(data,)).start()
    return {"status": "ok"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
