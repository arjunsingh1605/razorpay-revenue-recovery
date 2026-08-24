from data_loader import load_payments
from evaluate import evaluate_batch

payments=load_payments()
report=evaluate_batch(payments)

print("===== RECOVERY EVALUATION =====")
print("Total revenue at risk: ",report["total_at_risk"])
print("Retries: ",report["retry_count"])
print("Payment link actions: ",report["payment_link_count"])
print("Escalations: ",report["escalation_count"])
print("No action: ",report["no_action_count"])

print("\n===== PAYMENT DECISIONS =====")

for result in report["results"]:
    print(
        result["payment_id"],
        "₹" + str(result["amount"]),
        "->",
        result["action"]
    )

