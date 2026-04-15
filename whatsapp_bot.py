from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def open_whatsapp():
    s = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=s)

    print("Opening WhatsApp Web...")
    d.get("https://web.whatsapp.com")

    input("Scan QR → wait until chats fully load → then press Enter")

    return d


def send_message(d, contact, message):
    wait = WebDriverWait(d, 40)

    print("Waiting for search box...")

    search_box = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
    )

    search_box.click()
    search_box.send_keys(contact)
    search_box.send_keys(Keys.ENTER)

    print("Contact selected")

    msg_box = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@contenteditable="true"]'))
    )[-1]

    msg_box.click()
    msg_box.send_keys(message)
    msg_box.send_keys(Keys.ENTER)

    print("Message sent successfully")


if __name__ == "__main__":
    print("STARTING SCRIPT...")

    d = open_whatsapp()

    contact_name = "Ranjith"
    message_text = "hi"

    send_message(d, contact_name, message_text)