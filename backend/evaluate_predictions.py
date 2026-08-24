from data_loader import load_payments
from risk_scorer import calculate_recovery_probability
from recovery_pipeline import process_payment


payments = load_payments()

total_expected = 0
total_actual = 0

print("===== PREDICTION VS ACTUAL =====")

for payment in payments:

    probability = calculate_recovery_probability(payment)

    expected = payment["amount"] * probability

    result = process_payment(payment)

    actual = result["recovered_amount"]

    total_expected += expected
    total_actual += actual

    print(
        payment["payment_id"],
        "→ Probability:",
        f"{probability:.2f}",
        "→ Expected:",
        f"₹{expected:.2f}",
        "→ Actual:",
        f"₹{actual:.2f}"
    )


print("\n===== SUMMARY =====")
print("Expected recovery: ₹", round(total_expected, 2))
print("Actual recovery: ₹", round(total_actual, 2))