from data_loader import load_payments
from risk_scorer import calculate_recovery_probability

payments=load_payments()

for payment in payments:
    probability=calculate_recovery_probability(payment)

    expected_recovery=payment["amount"] * probability

    print(
        payment["payment_id"],
        "->",
        f"{probability:.2f}",
        "->",
        "Expected Recovery: ",
        f"{expected_recovery:.2f}"
    )
