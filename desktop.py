import pyautogui
import time
import subprocess

# === CONFIG (your coordinates) ===
SEARCH_X, SEARCH_Y = 265, 156
MSG_X, MSG_Y = 762, 1035


def open_whatsapp():
    print("Opening WhatsApp...")
    subprocess.Popen(
        "start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
        shell=True
    )
    time.sleep(6)  # wait for app to open


def send_message(contact, message):
    print("Clicking search box...")
    pyautogui.click(SEARCH_X, SEARCH_Y)
    time.sleep(1)

    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

    pyautogui.write(contact)
    time.sleep(1)
    pyautogui.press("enter")

    time.sleep(2)

    print("Typing message...")
    pyautogui.click(MSG_X, MSG_Y)
    time.sleep(1)

    pyautogui.write(message)
    pyautogui.press("enter")

    print("Message sent successfully")


if __name__ == "__main__":
    open_whatsapp()
    send_message("Ranjith", "hi")