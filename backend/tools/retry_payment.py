from recovery_simulator import simulate_recovery


def retry_payment(payment):
    """
    Attempt to recover a failed payment by retrying it.
    """

    if payment["status"] != "failed":
        return {
            "success": False,
            "message": "Payment is not failed.",
            "recovered_amount": 0
        }

    outcome = simulate_recovery(payment, "RETRY")

    return {
    "success": outcome["status"] == "SUCCESS",
    "payment_id": payment["payment_id"],
    "action": "RETRY",
    "status": outcome["status"],
    "recovered_amount": outcome["recovered_amount"],
    "message": "Payment successfully recovered through retry."
        if outcome["status"] == "SUCCESS"
        else "Retry failed."
}