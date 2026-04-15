from google import genai
from google.genai import types
from playwright.sync_api import sync_playwright
import time

c = genai.Client()

W, H = 1440, 900

def dx(x): return int(x/1000*W)
def dy(y): return int(y/1000*H)

def exec_fc(parts, p):
    executed = []

    for part in parts:
        if part.function_call:
            f = part.function_call
            n = f.name
            a = f.args

            print(f"Executing: {n} | args: {a}")

            try:
                if n == "click_at":
                    p.mouse.click(dx(a["x"]), dy(a["y"]))

                elif n == "type_text_at":
                    p.mouse.click(dx(a["x"]), dy(a["y"]))
                    p.keyboard.press("Control+A")
                    p.keyboard.press("Backspace")
                    p.keyboard.type(a["text"])
                    if a.get("press_enter", True):
                        p.keyboard.press("Enter")

                elif n == "scroll_document":
                    direction = a["direction"]
                    if direction == "down":
                        p.mouse.wheel(0, 800)
                    elif direction == "up":
                        p.mouse.wheel(0, -800)

                elif n == "navigate":
                    p.goto(a["url"])

                elif n == "wait_5_seconds":
                    time.sleep(5)

                else:
                    print(f"Skipped unsupported action: {n}")

            except Exception as e:
                print(f"Error executing {n}: {e}")

            executed.append(n)
            time.sleep(2)

    return executed

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=False)
    ctx = b.new_context(viewport={"width": W, "height": H})
    p = ctx.new_page()

    # ⚠️ Avoid Google to prevent CAPTCHA
    p.goto("https://news.ycombinator.com")

    cfg = types.GenerateContentConfig(
        tools=[types.Tool(computer_use=types.ComputerUse(
            environment=types.Environment.ENVIRONMENT_BROWSER
        ))]
    )

    s = p.screenshot(type="png")

    contents = [
        types.Content(role="user", parts=[
            types.Part(text="""
            You are controlling a browser.

            Goal:
            1. Scroll down the page
            2. Find a news article
            3. Click it
            4. If a PDF link is available, click it

            You MUST use function calls only.
            Do not explain.
            """),
            types.Part.from_bytes(data=s, mime_type="image/png")
        ])
    ]
    

    for step in range(5):
        print(f"\n--- Step {step+1} ---")

        r = c.models.generate_content(
            model="gemini-3-flash-preview",
            contents=contents,
            config=cfg
        )

        cand = r.candidates[0]
        contents.append(cand.content)

        has_fc = any(p.function_call for p in cand.content.parts)

        if not has_fc:
            txt = " ".join([p.text for p in cand.content.parts if p.text])
            print("Model stopped:", txt)
            break

        executed = exec_fc(cand.content.parts, p)

        # 🧠 Stop if nothing meaningful happened
        if not executed:
            print("No actions executed. Stopping.")
            break

        s = p.screenshot(type="png")

        frs = []
        for part in cand.content.parts:
            if part.function_call:
                fname = part.function_call.name

                frs.append(
                    types.FunctionResponse(
                        name=fname,
                        response={"url": p.url},
                        parts=[types.FunctionResponsePart(
                            inline_data=types.FunctionResponseBlob(
                                mime_type="image/png",
                                data=s
                            )
                        )]
                    )
                )

        contents.append(types.Content(
            role="user",
            parts=[types.Part(function_response=fr) for fr in frs]
        ))

    input("Press Enter to close...")
    b.close()