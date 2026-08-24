MAX_RETRIES=2

ALLOWED_ACTIONS={
    "RETRY","PAYMENT_LINK","ESCALATE","NO ACTION"
}

def validate_action(payment,action):
    if action not in ALLOWED_ACTIONS:
        return{
            "allowed":False,
            "reason":"Unknown recovery action"
        }
    if payment["status"]!="failed":
        return{
            "allowed":False,
            "reason":"Already successful"
        }
    if action == "RETRY" and payment["attempt_count"] >= MAX_RETRIES:
        return {
            "allowed": False,
            "reason": "Maximum retry limit reached."
        }

    return {
        "allowed": True,
        "reason": "Action passed all guardrails."
    }