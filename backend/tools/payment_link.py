import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

KEY_ID = os.getenv("RAZORPAY_KEY_ID")
KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

RAZORPAY_URL = "https://api.razorpay.com/v1/payment_links"


def create_payment_link(payment):
    if not KEY_ID or not KEY_SECRET:
        raise RuntimeError("Razorpay API keys are not configured.")

    payload = {
        "amount": int(payment["amount"]) * 100,
        "currency": payment.get("currency", "INR"),
        "accept_partial": False,
        "reference_id": f"recovery_{payment['payment_id']}_{int(__import__('time').time())}",
        "description": f"Payment recovery for {payment['payment_id']}",
        "expire_by": 0
    }

    response = requests.post(
        RAZORPAY_URL,
        auth=(KEY_ID, KEY_SECRET),
        json=payload,
        timeout=15
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"Razorpay API error: {response.status_code} {response.text}"
        )

    data = response.json()

    return {
        "action": "PAYMENT_LINK",
        "status": "PAYMENT_LINK_CREATED",
        "recovered_amount": 0,
        "message": "Razorpay Test Mode payment link created.",
        "payment_link": data.get("short_url"),
        "razorpay_payment_link_id": data.get("id")
    }


def fetch_payment_link(payment_link_id):
    response = requests.get(
        f"{RAZORPAY_URL}/{payment_link_id}",
        auth=(KEY_ID, KEY_SECRET),
        timeout=15
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Razorpay API error: {response.status_code} {response.text}"
        )

    return response.json()