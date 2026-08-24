def evaluate_payment(payment):
    if payment["status"] != "failed":
        return{
            "action":"NO ACTION",
            "reason":"payment already succesful"
        }
    if payment["attempt_count"]>3:
        return{
            "action":"ESCALATE",
            "reason":"Max retry attempts reached"
        }
    if payment["failure_reason"] in ["network_error","timeout","bank_error"]:
        if payment["previous_successful_payments"]>0:
               return{
                    "action":"RETRY",
                    "reason":"temporary failure, user has previous succesful payments"
               }
    if payment["failure_reason"] == "card_declined":
        return{
            "action":"PAYMENT_LINK",
            "reason":"Card declined, try an alternative payment method"
        }
    return{
         "action":"ESCALATE",
         "reason":"Failure reason cannot be safely handled automatically"
    } 