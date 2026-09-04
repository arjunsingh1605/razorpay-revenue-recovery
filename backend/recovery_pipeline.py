from recovery_engine import evaluate_payment
from risk_scorer import calculate_recovery_probability
from audit_logger import log_event
from tool_executer import execute_action
from llm.agent import get_recovery_decision


def process_payment(payment):
    probability = calculate_recovery_probability(payment)
    decision = get_recovery_decision(payment)

    outcome = execute_action(
        payment,
        decision["action"],
        decision["reason"]
    )

    result = {
        "payment_id": payment["payment_id"],
        "amount": payment["amount"],
        "recovery_probability": probability,
        "action": outcome.get("action", decision["action"]),
        "reason": outcome.get("message", decision["reason"]),
        "status": outcome["status"],
        "recovered_amount": outcome["recovered_amount"],
        "confidence": decision["confidence"],
        "payment_link": outcome.get("payment_link"),
        "razorpay_payment_link_id": outcome.get("razorpay_payment_link_id"),
    }

    log_event(result)
    return result