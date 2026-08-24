import json
from pathlib import Path

def load_payments():
    file_path=Path(__file__).parent.parent / "data" / "payments.json"

    with open(file_path,"r",encoding="utf-8") as file:
        payments=json.load(file)

    return payments

