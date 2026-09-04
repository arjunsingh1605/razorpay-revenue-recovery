from llm.agent import get_recovery_decision


payment = {
    "payment_id": "TEST001",
    "amount": 2499,
    "currency": "INR",
    "status": "failed",
    "failure_reason": "network_error",
    "attempt_count": 1,
    "previous_successful_payments": 6,
    "previous_failed_payments": 1,
    "total_previous_spend": 18500
}


decision = get_recovery_decision(payment)

print("LLM DECISION")
print("Action:", decision["action"])
print("Reason:", decision["reason"])
print("Confidence:", decision["confidence"])