import undetected_chromedriver as uc
import time

print("Initializing driver...")
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
try:
    driver = uc.Chrome(options=options, headless=False)
    print("Driver initialized.")
    driver.get("https://www.google.com")
    print("Navigated to Google.")
    time.sleep(5)
    driver.quit()
    print("Done.")
except Exception as e:
    print(f"Error: {e}")
