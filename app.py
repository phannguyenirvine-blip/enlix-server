from flask import Flask, request
import os, json, threading

app = Flask(__name__)

def process_webhook(data):
    """Xử lý dữ liệu webhook tách riêng (chạy nền, không làm Zalo chờ)"""
    print("\n🔍 WEBHOOK DEBUG — DỮ LIỆU NHẬN ĐƯỢC TỪ ZALO:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    # (ở bước sau, bạn sẽ thêm xử lý dịch, phản hồi...)

@app.route("/")
def home():
    return "🟢 EnlixS đang hoạt động — Webhook OK"

@app.route("/webhook/zalo", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("verify_token")
        return verify_token or "OK", 200

    try:
        data = request.get_json(silent=True)
        # chạy xử lý nền để không chặn response 200
        threading.Thread(target=process_webhook, args=(data,)).start()
    except Exception as e:
        print("❌ Lỗi nhận webhook:", e)
    # trả về 200 ngay lập tức cho Zalo
    return {"status": "ok"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
