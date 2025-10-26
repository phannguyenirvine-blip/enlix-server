from flask import Flask, request
import os, json

app = Flask(__name__)

@app.route("/")
def home():
    return "🟢 Enlix Server debug mode — waiting for Zalo webhook"

@app.route("/webhook/zalo", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return request.args.get("verify_token", ""), 200

    data = request.get_json(silent=True)
    print("\n🔍 WEBHOOK DEBUG — DỮ LIỆU NHẬN ĐƯỢC TỪ ZALO:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return {"ok": True}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
