from fastapi import APIRouter, HTTPException
from recovery_pipeline import process_payment
from tools.payment_link import fetch_payment_link

router = APIRouter(prefix="/api/recovery")


PAYMENTS = {
    "TEST001": {
        "payment_id": "TEST001",
        "amount": 2499,
        "currency": "INR",
        "status": "failed",
        "failure_reason": "network_error",
        "attempt_count": 1,
        "previous_successful_payments": 6,
        "previous_failed_payments": 1,
        "total_previous_spend": 18500
    },

    "TEST002": {
        "payment_id": "TEST002",
        "amount": 8999,
        "currency": "INR",
        "status": "failed",
        "failure_reason": "card_declined",
        "attempt_count": 2,
        "previous_successful_payments": 4,
        "previous_failed_payments": 2,
        "total_previous_spend": 32000
    },

    "TEST003": {
        "payment_id": "TEST003",
        "amount": 75000,
        "currency": "INR",
        "status": "failed",
        "failure_reason": "multiple_failures",
        "attempt_count": 3,
        "previous_successful_payments": 1,
        "previous_failed_payments": 5,
        "total_previous_spend": 75000
    },

    "TEST004": {
        "payment_id": "TEST004",
        "amount": 1499,
        "currency": "INR",
        "status": "failed",
        "failure_reason": "timeout",
        "attempt_count": 1,
        "previous_successful_payments": 8,
        "previous_failed_payments": 0,
        "total_previous_spend": 24000
    },

    "TEST005": {
        "payment_id": "TEST005",
        "amount": 4999,
        "currency": "INR",
        "status": "failed",
        "failure_reason": "insufficient_funds",
        "attempt_count": 1,
        "previous_successful_payments": 3,
        "previous_failed_payments": 1,
        "total_previous_spend": 12000
    }
}


@router.post("/analyze")
def analyze_payment(payment: dict):

    payment_id = payment.get("payment_id")

    if payment_id not in PAYMENTS:
        raise HTTPException(
            status_code=404,
            detail=f"Payment {payment_id} not found."
        )

    payment_data = PAYMENTS[payment_id]

    result = process_payment(payment_data)

    return result

@router.get("/verify/{payment_link_id}")
def verify_payment(payment_link_id: str):
    try:
        data = fetch_payment_link(payment_link_id)

        return {
            "status": data.get("status"),
            "amount_paid": data.get("amount_paid", 0) / 100,
            "payment_link_id": data.get("id")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )