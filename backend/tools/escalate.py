def escalate_to_human(payment, reason):
    """
    Escalate a payment to a human support/recovery team.
    """

    return {
        "success": True,
        "payment_id": payment["payment_id"],
        "action": "ESCALATE",
        "status": "ESCALATED",
        "recovered_amount": 0,
        "message": reason
    }