import pyautogui
import time
import subprocess
import re
import pygetwindow as gw

def open_whatsapp():
    print("Opening WhatsApp...")

    subprocess.Popen(
        "start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
        shell=True
    )

    time.sleep(5)

    # bring WhatsApp window to front
    windows = gw.getWindowsWithTitle("WhatsApp")

    if windows:
        windows[0].activate()
        windows[0].maximize()
        print("WhatsApp focused")
    else:
        print("WhatsApp window not found")

# === COORDINATES ===
SEARCH_X, SEARCH_Y = 265, 156
MSG_X, MSG_Y = 762, 1035


# ===== PARSER =====
def parse_command(c):
    c = c.lower().strip()

    m1 = re.search(r"(text|send|message)\s+(.*?)\s+to\s+(.*)", c)
    m2 = re.search(r"(text|send|message)\s+to\s+(.*?)\s+(.*)", c)

    if m1:
        return {
            "intent": "send_message",
            "contact": m1.group(3),
            "message": m1.group(2)
        }

    if m2:
        return {
            "intent": "send_message",
            "contact": m2.group(2),
            "message": m2.group(3)
        }

    return {"intent": "unknown"}


# ===== AUTOMATION =====
def open_whatsapp():
    subprocess.Popen(
        "start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
        shell=True
    )
    time.sleep(6)


def send_message(contact, message):
    pyautogui.click(SEARCH_X, SEARCH_Y)
    time.sleep(1)

    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

    pyautogui.write(contact)
    time.sleep(1)
    pyautogui.press("enter")

    time.sleep(2)

    pyautogui.click(MSG_X, MSG_Y)
    time.sleep(1)

    pyautogui.write(message)
    pyautogui.press("enter")


# ===== MAIN =====
if __name__ == "__main__":
    cmd = input("Enter command: ")

    res = parse_command(cmd)

    if res["intent"] == "send_message":
        open_whatsapp()
        send_message(res["contact"], res["message"])
    else:
        print("Unknown command")