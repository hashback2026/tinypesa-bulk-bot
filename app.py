import os
import requests
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# TinyPesa Configuration
TINYPESA_API_URL = os.getenv('TINYPESA_API_URL', 'https://api.tinypesa.com/api/v1')
TINYPESA_USERNAME = os.getenv('TINYPESA_USERNAME')
TINYPESA_API_KEY = os.getenv('TINYPESA_API_KEY')

def send_stk_push(phone, amount, account_ref="BulkPayment"):
    """
    Send STK Push via TinyPesa API
    Format phone: 2547XXXXXXXX
    """
    url = f"{TINYPESA_API_URL}/express/initialize"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "username": TINYPESA_USERNAME,
        "api_key": TINYPESA_API_KEY,
        "phone": phone,
        "amount": amount,
        "account_no": account_ref
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status": "failed"}

def format_phone(phone):
    """Convert various formats to 2547XXXXXXXX"""
    phone = phone.strip().replace(" ", "").replace("-", "")

    if phone.startswith("+254"):
        return phone[1:]
    elif phone.startswith("0"):
        return "254" + phone[1:]
    elif phone.startswith("254"):
        return phone
    elif len(phone) == 9 and phone.startswith("7"):
        return "254" + phone
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send-bulk', methods=['POST'])
def send_bulk():
    data = request.get_json()
    phones = data.get('phones', [])
    amount = data.get('amount', 0)
    account_ref = data.get('account_ref', 'BulkPayment')

    if not phones or amount <= 0:
        return jsonify({"error": "Invalid input"}), 400

    results = []
    success_count = 0
    failed_count = 0

    for phone in phones:
        formatted = format_phone(phone)

        if not formatted:
            results.append({
                "original": phone,
                "status": "failed",
                "message": "Invalid phone format"
            })
            failed_count += 1
            continue

        # Send STK Push
        response = send_stk_push(formatted, amount, account_ref)

        if response.get('error'):
            results.append({
                "original": phone,
                "formatted": formatted,
                "status": "failed",
                "message": response.get('error')
            })
            failed_count += 1
        else:
            results.append({
                "original": phone,
                "formatted": formatted,
                "status": "success",
                "response": response
            })
            success_count += 1

    return jsonify({
        "total": len(phones),
        "successful": success_count,
        "failed": failed_count,
        "results": results
    })

@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle TinyPesa payment callbacks"""
    data = request.get_json()
    print(f"Webhook received: {json.dumps(data, indent=2)}")

    # TODO: Update your database/payment records here
    # Check data.get('status') for 'success' or 'failed'

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
