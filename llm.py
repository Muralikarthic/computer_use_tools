import pyautogui
import time
import subprocess
import json
import re
from google import genai

# ===== CONFIG =====
API_KEY = "MY_API_KEY"

SEARCH_X, SEARCH_Y = 265, 156
MSG_X, MSG_Y = 762, 1035

# ===== GEMINI SETUP =====
client = genai.Client(api_key=API_KEY)


# ===== JSON EXTRACTOR =====
def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {"intent": "unknown"}


# ===== LLM PARSER =====
def parse_command_llm(command):
    prompt = f"""
Convert the user input into JSON with:
intent, contact, message

Only return JSON.

Example:
text hi to ranjith
{{"intent":"send_message","contact":"ranjith","message":"hi"}}

Now parse:
{command}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    print("RAW RESPONSE:", response.text)
    
    return extract_json(response.text)


# ===== AUTOMATION =====
def open_whatsapp():
    subprocess.Popen(
        "start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
        shell=True
    )
    time.sleep(6)


def send_message(contact, message):
    # click search box
    pyautogui.click(SEARCH_X, SEARCH_Y)
    time.sleep(1)

    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

    pyautogui.write(contact)
    time.sleep(1)
    pyautogui.press("enter")

    time.sleep(2)

    # click message box
    pyautogui.click(MSG_X, MSG_Y)
    time.sleep(1)

    pyautogui.write(message)
    pyautogui.press("enter")

    print("Message sent successfully")


# ===== MAIN LOOP =====
if __name__ == "__main__":
    print("AI Assistant Started")

    while True:
        cmd = input("Enter command: ")

        res = parse_command_llm(cmd)
        print("Parsed:", res)

        if res.get("intent") == "send_message":
            open_whatsapp()
            send_message(res.get("contact"), res.get("message"))
        else:
            print("Unknown command")