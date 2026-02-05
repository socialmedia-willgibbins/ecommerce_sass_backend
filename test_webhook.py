#!/usr/bin/env python3
"""
Test script for Razorpay webhook
Simulates a payment.captured event with proper signature
"""

import requests
import hmac
import hashlib
import json

# Configuration
WEBHOOK_URL = "https://helmstonegroup.com/api/orders/razorpay-webhook/"
WEBHOOK_SECRET = "helmstone123"  # Your webhook secret (from VPS .env)

# Test payload - payment.captured event
payload = {
    "entity": "event",
    "account_id": "acc_test123",
    "event": "payment.captured",
    "contains": ["payment"],
    "payload": {
        "payment": {
            "entity": {
                "id": "pay_test_12345678",
                "entity": "payment",
                "amount": 50000,  # ₹500.00 (in paise)
                "currency": "INR",
                "status": "captured",
                "order_id": "order_test_123",
                "method": "card",
                "email": "test@example.com",
                "contact": "+919876543210",
                "notes": {
                    "order_id": "1"  # Your internal order ID
                },
                "created_at": 1643723400
            }
        }
    },
    "created_at": 1643723400
}

# Convert payload to JSON string
payload_string = json.dumps(payload, separators=(',', ':'))

# Generate HMAC signature
signature = hmac.new(
    WEBHOOK_SECRET.encode('utf-8'),
    payload_string.encode('utf-8'),
    hashlib.sha256
).hexdigest()

print("=" * 60)
print("Testing Razorpay Webhook")
print("=" * 60)
print(f"\n📡 Webhook URL: {WEBHOOK_URL}")
print(f"🔑 Secret: {WEBHOOK_SECRET}")
print(f"📦 Event: payment.captured")
print(f"💰 Amount: ₹500.00")
print(f"✍️  Signature: {signature[:20]}...")
print("\n" + "=" * 60)

# Send POST request
headers = {
    'Content-Type': 'application/json',
    'X-Razorpay-Signature': signature
}

print("\n🚀 Sending webhook request...\n")

try:
    response = requests.post(
        WEBHOOK_URL,
        data=payload_string,
        headers=headers,
        timeout=10
    )
    
    print(f"✅ Response Status: {response.status_code}")
    print(f"📄 Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ Webhook test SUCCESSFUL!")
        print("Check backend logs: pm2 logs helmstone-backend")
    else:
        print(f"\n❌ Webhook test FAILED!")
        print(f"Status: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ Request failed: {str(e)}")
    print("Make sure the VPS backend is running!")

print("\n" + "=" * 60)

# Test payment.failed event
print("\n\n" + "=" * 60)
print("Testing payment.failed event")
print("=" * 60)

failed_payload = {
    "entity": "event",
    "account_id": "acc_test123",
    "event": "payment.failed",
    "contains": ["payment"],
    "payload": {
        "payment": {
            "entity": {
                "id": "pay_test_failed123",
                "entity": "payment",
                "amount": 30000,
                "currency": "INR",
                "status": "failed",
                "order_id": "order_test_456",
                "method": "card",
                "email": "test@example.com",
                "contact": "+919876543210",
                "error_code": "BAD_REQUEST_ERROR",
                "error_description": "Payment processing failed due to insufficient funds",
                "error_reason": "insufficient_funds",
                "notes": {},
                "created_at": 1643723500
            }
        }
    },
    "created_at": 1643723500
}

failed_payload_string = json.dumps(failed_payload, separators=(',', ':'))
failed_signature = hmac.new(
    WEBHOOK_SECRET.encode('utf-8'),
    failed_payload_string.encode('utf-8'),
    hashlib.sha256
).hexdigest()

print(f"\n📦 Event: payment.failed")
print(f"💰 Amount: ₹300.00")
print(f"❌ Reason: insufficient_funds")
print("\n🚀 Sending webhook request...\n")

try:
    response = requests.post(
        WEBHOOK_URL,
        data=failed_payload_string,
        headers={
            'Content-Type': 'application/json',
            'X-Razorpay-Signature': failed_signature
        },
        timeout=10
    )
    
    print(f"✅ Response Status: {response.status_code}")
    print(f"📄 Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ Failed payment webhook test SUCCESSFUL!")
    else:
        print(f"\n❌ Webhook test FAILED!")
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ Request failed: {str(e)}")

print("\n" + "=" * 60)
print("\n💡 To view backend logs:")
print("   ssh deploy@89.116.121.93")
print("   pm2 logs helmstone-backend --lines 50")
print("=" * 60)
