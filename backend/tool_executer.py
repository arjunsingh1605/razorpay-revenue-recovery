from guardrails import validate_action

from tools.retry_payment import retry_payment
from tools.payment_link import create_payment_link
from tools.escalate import escalate_to_human


def execute_action(payment, action, reason=""):
    """
    Validate and execute a recovery action.
    """

    validation = validate_action(
        payment,
        action
    )

    if not validation["allowed"]:
        return escalate_to_human(
            payment,
            validation["reason"]
        )

    if action == "RETRY":
        return retry_payment(payment)

    if action == "PAYMENT_LINK":
        return create_payment_link(payment)

    if action == "ESCALATE":
        return escalate_to_human(
            payment,
            reason
        )

    if action == "NO_ACTION":
        return {
            "success": True,
            "payment_id": payment["payment_id"],
            "action": "NO_ACTION",
            "status": "NOT_ATTEMPTED",
            "recovered_amount": 0,
            "message": "No recovery action required."
        }

    return escalate_to_human(
        payment,
        "Unknown action."
    )   