import pyautogui
import time
import subprocess
import json
import re
from google import genai
from google.genai import errors

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
# ===== LLM PARSER =====
def parse_command_llm(command, retries=0, max_retries=2):
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

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )

        print("RAW RESPONSE:", response.text)
        return extract_json(response.text)

    except errors.ClientError as e:
        if e.code == 429:
            # Check if we have tried too many times
            if retries >= max_retries:
                print("\n[!] Still getting rate limited. You have likely hit your DAILY quota limit.")
                print("[!] Check https://ai.dev/rate-limit or try again tomorrow.")
                return {"intent": "unknown"}

            print(f"\n[!] Rate limit hit! Waiting 60 seconds... (Attempt {retries + 1} of {max_retries})")
            time.sleep(60)
            
            # Call itself again, but increase the retry counter
            return parse_command_llm(command, retries=retries + 1, max_retries=max_retries)
            
        else:
            print(f"An unexpected API error occurred: {e}")
            return {"intent": "unknown"}

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