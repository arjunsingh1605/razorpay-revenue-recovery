from recovery_engine import evaluate_payment
from recovery_simulator import simulate_recovery

def process_payment(payment):
    decision=evaluate_payment(payment)
    outcome=simulate_recovery(
       payment,
       decision["action"]
    )

    return {
        "payment_id": payment["payment_id"],
        "amount": payment["amount"],
        "action": decision["action"],
        "reason": decision["reason"],
        "status": outcome["status"],
        "recovered_amount": outcome["recovered_amount"]
    }