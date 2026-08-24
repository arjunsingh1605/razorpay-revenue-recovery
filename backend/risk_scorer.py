def calculate_recovery_probability(payment):
    if payment["status"] != "failed":
        return 0.0

    score=0.0

    if payment["failure_reason"] in ["network_error","timeout","bank_error"]:
        score += 0.5

    elif payment["failure_reason"] == "card_declined":
        score += 0.1

    else: score += 0.2



    if payment["previous_successful_payments"] >=5:
        score+=0.3
    elif payment["previous_successful_payments"] >=2:
        score += 0.2
    elif payment["previous_successful_payments"] ==1:
        score +=0.1


    if payment["attempt_count"] == 1:
       score+=0.2
    elif payment["attempt_count"] == 2:
       score+=0.1

    return min(score,0.9)
    
    
