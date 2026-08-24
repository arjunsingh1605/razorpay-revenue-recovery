from data_loader import load_payments
from recovery_engine import evaluate_payment

payments=load_payments()

for payment in payments:
    result=evaluate_payment(payment)
    print(
        payment["payment_id"],
        "->",
        result["action"],
        "->",
        result["reason"]
    )