from flask import Flask, request, jsonify
import razorpay
import os

app = Flask(__name__)

client = razorpay.Client(
    auth=(
        os.environ["RAZORPAY_KEY_ID"],
        os.environ["RAZORPAY_KEY_SECRET"]
    )
)

@app.route("/")
def health():
    return "Backend running on Fly.io", 200

@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.json
    order = client.order.create({
        "amount": int(data["amount"]) * 100,
        "currency": "INR",
        "payment_capture": 1
    })
    return jsonify(order)

@app.route("/verify-webhook", methods=["POST"])
def verify_webhook():
    payload = request.data.decode()
    signature = request.headers.get("X-Razorpay-Signature")

    try:
        razorpay.utility.verify_webhook_signature(
            payload,
            signature,
            os.environ["RAZORPAY_WEBHOOK_SECRET"]
        )
        return "OK", 200
    except:
        return "Invalid", 400
