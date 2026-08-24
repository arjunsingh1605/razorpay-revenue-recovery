import json
from pathlib import Path

AUDIT_FILE=Path(__file__).parent.parent / "data" / "audit_log.json"

def log_event(event):
    if AUDIT_FILE.exists():
        with open(AUDIT_FILE,"r",encoding="utf-8") as file:
            events=json.load(file)

    else:
        events=[]

    events.append(event)

    with open(AUDIT_FILE,"w",encoding="utf-8") as file:
            json.dump(events,file,indent=2)

