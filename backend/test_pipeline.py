from data_loader import load_payments
from recovery_pipeline import process_payment

payments=load_payments()
for payment in payments:
    result=process_payment(payment)
    print(
        result["payment_id"],
        "->",
        result["action"],
        "->",
        result["status"],
        "->",
        "RECOVERED: ", result["recovered_amount"]
    )