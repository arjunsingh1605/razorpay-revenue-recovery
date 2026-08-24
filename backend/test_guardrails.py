from data_loader import load_payments
from recovery_engine import evaluate_payment
from guardrails import validate_action


payments = load_payments()

for payment in payments:

    decision = evaluate_payment(payment)

    validation = validate_action(
        payment,
        decision["action"]
    )

    print(
        payment["payment_id"],
        "→",
        decision["action"],
        "→",
        validation["allowed"],
        "→",
        validation["reason"]
    )