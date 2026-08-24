from recovery_engine import evaluate_payment
from recovery_simulator import simulate_recovery
from risk_scorer import calculate_recovery_probability
from audit_logger import log_event
from guardrails import validate_action

def process_payment(payment):
    probability = calculate_recovery_probability(payment)
    decision=evaluate_payment(payment)

    validation = validate_action(
        payment,
        decision["action"]
    )

    if not validation["allowed"]:
        result = {
            "payment_id": payment["payment_id"],
            "amount": payment["amount"],
            "recovery_probability": probability,
            "action": "ESCALATE",
            "reason": validation["reason"],
            "status": "ESCALATED",
            "recovered_amount": 0
        }

        log_event(result)

        return result
    
    outcome=simulate_recovery(
       payment,
       decision["action"]
    )

    result= {
        "payment_id": payment["payment_id"],
        "amount": payment["amount"],
        "recovery_probability": probability,
        "action": decision["action"],
        "reason": decision["reason"],
        "status": outcome["status"],
        "recovered_amount": outcome["recovered_amount"]
    }

    log_event(result)
    return result