def simulate_recovery(payment, action):
    if action == "NO_ACTION":
        return {
            "status": "NOT_ATTEMPTED",
            "recovered_amount": 0
        }

    if action == "ESCALATE":
        return {
            "status": "ESCALATED",
            "recovered_amount": 0
        }

    if action == "RETRY":
        if payment["failure_reason"] in [
            "network_error",
            "timeout",
            "bank_error"
        ]:
            return {
                "status": "SUCCESS",
                "recovered_amount": payment["amount"]
            }

        return {
            "status": "FAILED",
            "recovered_amount": 0
        }

    if action == "PAYMENT_LINK":
        if payment["previous_successful_payments"] > 0:
            return {
                "status": "SUCCESS",
                "recovered_amount": payment["amount"]
            }

        return {
            "status": "FAILED",
            "recovered_amount": 0
        }

    return {
        "status": "FAILED",
        "recovered_amount": 0
    }