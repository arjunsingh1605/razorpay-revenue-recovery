from openai import OpenAI
import json

ALLOWED_ACTIONS = {
    "RETRY",
    "PAYMENT_LINK",
    "ESCALATE"
}

client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key="not-needed"
)


def get_recovery_decision(payment):

    prompt = f"""
You are a payment recovery decision agent.

Analyze this failed payment and choose exactly ONE action:

RETRY
PAYMENT_LINK
ESCALATE

Payment information:
Payment ID: {payment["payment_id"]}
Amount: {payment["amount"]} {payment["currency"]}
Failure reason: {payment["failure_reason"]}
Attempt count: {payment["attempt_count"]}
Previous successful payments: {payment["previous_successful_payments"]}
Previous failed payments: {payment["previous_failed_payments"]}
Previous total spend: {payment["total_previous_spend"]}

Return ONLY valid JSON in this format:

{{
    "action": "RETRY",
    "reason": "short explanation",
    "confidence": 0.0
}}

Confidence must be a number between 0 and 1.
"""

    response = client.chat.completions.create(
        model="auto/best-free",
        messages=[
            {
                "role": "system",
                "content": "You are a payment recovery decision agent."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    # Remove markdown code fences if the model adds them
    content = content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    decision = json.loads(content)

    # Validate action
    if decision["action"] not in ALLOWED_ACTIONS:
        raise ValueError(
            f"Invalid LLM action: {decision['action']}"
        )

    # Validate confidence
    confidence = decision["confidence"]

    if not 0 <= confidence <= 1:
        raise ValueError(
            f"Invalid confidence: {confidence}"
        )

    if confidence < 0.5:
     decision["action"] = "ESCALATE"
     decision["reason"] = (
        "LLM confidence was too low for automatic recovery."
    )

    return decision