from data_loader import load_payments

from tools.retry_payment import retry_payment
from tools.payment_link import create_payment_link
from tools.escalate import escalate_to_human


payments = load_payments()

for payment in payments:

    if payment["status"] != "failed":
        continue

    retry_result = retry_payment(payment)

    link_result = create_payment_link(payment)

    escalation_result = escalate_to_human(
        payment,
        "Testing escalation tool."
    )

    print("\n", payment["payment_id"])

    print(
        "RETRY:",
        retry_result
    )

    print(
        "PAYMENT LINK:",
        link_result
    )

    print(
        "ESCALATE:",
        escalation_result
    )