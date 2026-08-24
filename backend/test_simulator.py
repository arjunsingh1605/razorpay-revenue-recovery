from data_loader import load_payments
from recovery_engine import evaluate_payment
from recovery_simulator import simulate_recovery


payments = load_payments()

total_recovered = 0

for payment in payments:
    decision = evaluate_payment(payment)

    outcome = simulate_recovery(
        payment,
        decision["action"]
    )

    total_recovered += outcome["recovered_amount"]

    print(
        payment["payment_id"],
        "->",
        decision["action"],
        "->",
        outcome["status"],
        "-> ₹" + str(outcome["recovered_amount"])
    )

print("\nTotal recovered: ₹", total_recovered)