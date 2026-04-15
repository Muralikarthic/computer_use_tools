import re

def parse_command(c):
    c = c.lower().strip()

    # OPEN APP
    if any(k in c for k in ["open", "launch", "start"]):
        w = c.split()
        for i in range(len(w)):
            if w[i] in ["open", "launch", "start"] and i+1 < len(w):
                return {
                    "intent": "open_app",
                    "app": w[i+1]
                }

    # SEND MESSAGE (multiple patterns)

    # pattern 1: "text hi to ranjith"
    m1 = re.search(r"(text|message|send)\s+(.*?)\s+to\s+(.*)", c)

    # pattern 2: "text to ranjith hi"
    m2 = re.search(r"(text|message|send)\s+to\s+(.*?)\s+(.*)", c)

    # pattern 3: "send ranjith hi"
    m3 = re.search(r"(text|message|send)\s+(.*?)\s+(.*)", c)

    if m1:
        return {
            "intent": "send_message",
            "app": "whatsapp",
            "message": m1.group(2),
            "contact": m1.group(3)
        }

    if m2:
        return {
            "intent": "send_message",
            "app": "whatsapp",
            "contact": m2.group(2),
            "message": m2.group(3)
        }

    if m3:
        return {
            "intent": "send_message",
            "app": "whatsapp",
            "contact": m3.group(2),
            "message": m3.group(3)
        }

    return {"intent": "unknown"}

tests = [
    "open   whatsapp",
    "start spotify app",
    "text to ranjith hi",
    "send ranjith hello",
    "message hi ranjith"
]

for t in tests:
    print("INPUT:", t)
    print("OUTPUT:", parse_command(t))
    print("-" * 40)