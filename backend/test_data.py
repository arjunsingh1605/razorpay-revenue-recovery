from data_loader import load_payments

payments=load_payments()

print("Total Payments: ", len(payments))

for payment in payments:
    print(
        payment["payment_id"],
        "₹"+str(payment["amount"]),
        payment["status"]
    )