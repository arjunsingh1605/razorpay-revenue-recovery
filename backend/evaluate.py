from data_loader import load_payments
from recovery_engine import evaluate_payment

def evaluate_batch(payments):
    results=[]  

    total_at_risk=0
    retry_count=0
    payment_link_count=0
    escalation_count=0
    no_action_count=0

    for payment in payments:
        result=evaluate_payment(payment)

        if payment["status"] == "failed":
            total_at_risk+=1
        if result["action"]== "RETRY":
            retry_count+=1
        elif result["action"]=="PAYMENT_LINK":
            payment_link_count+=1
        elif result["action"]=="ESCALATE":
            escalation_count+=1
        elif result["action"]=="NO_ACTION":
            no_action_count+=1

        results.append({
            "payment_id": payment["payment_id"],
            "amount": payment["amount"],
            "action": result["action"],
            "reason": result["reason"]
       })

    return {
        "total_at_risk": total_at_risk,
        "retry_count": retry_count,
        "payment_link_count": payment_link_count,
        "escalation_count": escalation_count,
        "no_action_count": no_action_count,
        "results": results
    }