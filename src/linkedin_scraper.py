import os
import time
import warnings
import re
import json
import pickle
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Ignore warnings
warnings.filterwarnings("ignore")

# Load environment variables from .env
load_dotenv()

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Optional: run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\t+', '\t', text)
    text = re.sub(r'\t\s+', ' ', text)
    text = re.sub(r'\n\s+', '\n', text)
    return text

def remove_duplicates(text):
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        if line[:len(line)//2] == line[len(line)//2:]:
            new_lines.append(line[:len(line)//2])
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

def scroll_logic(web_driver):
    last_height = web_driver.execute_script("return document.body.scrollHeight")
    for _ in range(15):
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = web_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def save_cookies(driver, path):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("🍪 Cookies saved!")

def load_cookies(driver, path, url="https://www.linkedin.com/"):
    driver.get(url)
    with open(path, "rb") as file:
        cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("🍪 Cookies loaded!")

def login_with_cookies(driver, cookie_path):
    if os.path.exists(cookie_path):
        try:
            load_cookies(driver, cookie_path)
            driver.get("https://www.linkedin.com/feed/")
            time.sleep(5)
            if "feed" in driver.current_url:
                print("✅ Logged in using cookies")
                return True
        except Exception as e:
            print("⚠️ Cookie load failed. Proceeding with manual login:", e)

    driver.get("https://www.linkedin.com/login")
    print("🔐 Please log in manually in the opened browser")

    while True:
        user_input = input("⏳ Type 'start' after completing login + verification: ").strip().lower()
        if user_input == "start":
            save_cookies(driver, cookie_path)
            print("✅ Manual login complete and cookies saved.")
            return True
        else:
            print("❗ Invalid input. Type 'start' when done logging in.")

def generic_scraper(web_driver, url, main_div_class, content_div_class, output_key_name, output_filename):
    web_driver.get(url)
    time.sleep(5)
    scroll_logic(web_driver)
    time.sleep(5)

    try:
        soup = BeautifulSoup(web_driver.page_source, "lxml")
    except Exception:
        soup = BeautifulSoup(web_driver.page_source, "html.parser")

    main_div = soup.find("div", {"class": main_div_class}) or soup.find("main", {"class": main_div_class})
    content_divs = main_div.find_all("div", {"class": content_div_class}) if main_div else []

    text_data = [remove_duplicates(clean_text(div.get_text())) for div in content_divs]
    json_data = [{"id": i, output_key_name: text} for i, text in enumerate(text_data)]

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Saved to {output_filename}")
    return json_data

def scrape_profile_page(web_driver, profile_url, person_name):
    web_driver.get(profile_url)
    time.sleep(5)
    scroll_logic(web_driver)
    time.sleep(5)

    try:
        soup = BeautifulSoup(web_driver.page_source, "lxml")
    except Exception:
        soup = BeautifulSoup(web_driver.page_source, "html.parser")

    profile_main = soup.find("main", {"class": "KvRJXMpQfKwEcgEcBArUUlCAbTXLQvCpWmSxM"})
    profile_sections = profile_main.find_all("section", {"class": "artdeco-card"}) if profile_main else []

    text_data = [remove_duplicates(clean_text(sec.get_text())) for sec in profile_sections]
    json_data = [{"id": i, "profile_text_data": text} for i, text in enumerate(text_data)]

    with open(f"./data/{person_name}/profile_text_data.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print("✅ Saved to profile_text_data.json")
    return json_data

def scrape_experience(web_driver, profile_url, person_name):
    return generic_scraper(
        web_driver,
        profile_url + "details/experience/",
        "scaffold-finite-scroll__content",
        "LWlsiCwfBojCMKjczOoYFrNXHLWLZQzJZPw hXSIBQFiZpUIAllWMsrCQfCDXgDjwnBGodc BOWvRyXFbKrnuISjECjeIPpaGdtYghySFZyeA",
        "experience_text_data",
        f"./data/{person_name}/experience_text_data.json"
    )

def scrape_education(web_driver, profile_url, person_name):
    return generic_scraper(
        web_driver,
        profile_url + "details/education/",
        "scaffold-finite-scroll__content",
        "LWlsiCwfBojCMKjczOoYFrNXHLWLZQzJZPw hXSIBQFiZpUIAllWMsrCQfCDXgDjwnBGodc BOWvRyXFbKrnuISjECjeIPpaGdtYghySFZyeA",
        "education_text_data",
        f"./data/{person_name}/education_text_data.json"
    )

def scrape_certifications(web_driver, profile_url, person_name):
    return generic_scraper(
        web_driver,
        profile_url + "details/certifications/",
        "scaffold-finite-scroll__content",
        "LWlsiCwfBojCMKjczOoYFrNXHLWLZQzJZPw hXSIBQFiZpUIAllWMsrCQfCDXgDjwnBGodc BOWvRyXFbKrnuISjECjeIPpaGdtYghySFZyeA",
        "certifications_text_data",
        f"./data/{person_name}/certifications_text_data.json"
    )

def scrape_recent_activity(web_driver, profile_url, person_name):
    return generic_scraper(
        web_driver,
        profile_url + "recent-activity/all/",
        "KvRJXMpQfKwEcgEcBArUUlCAbTXLQvCpWmSxM",
        "update-components-text relative update-components-update-v2__commentary",
        "activities_text_data",
        f"./data/{person_name}/activities_text_data.json"
    )

def combine_all_data(person_name, *all_data_lists):
    combined_data = {}
    for data_list in all_data_lists:
        for item in data_list:
            for key, value in item.items():
                if key == "id":
                    continue
                if key not in combined_data:
                    combined_data[key] = []
                combined_data[key].append(value)

    with open(f"./data/{person_name}/final_profile.json", "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4, ensure_ascii=False)

    print("🎉 All data combined and saved to final_profile.json")

def scrape_full_profile(web_driver, profile_url, person_name="taufeeq"):
    os.makedirs(f"./data/{person_name}", exist_ok=True)

    profile_data = scrape_profile_page(web_driver, profile_url, person_name)
    experience_data = scrape_experience(web_driver, profile_url, person_name)
    education_data = scrape_education(web_driver, profile_url, person_name)
    certifications_data = scrape_certifications(web_driver, profile_url, person_name)
    activity_data = scrape_recent_activity(web_driver, profile_url, person_name)

    combine_all_data(person_name, profile_data, experience_data, education_data, certifications_data, activity_data)

if __name__ == "__main__":
    profile_url = "https://www.linkedin.com/in/taufeeq/"
    person_name = "Taufeeq"
    cookie_path = "./cookies/linkedin_cookies.pkl"

    os.makedirs("./cookies", exist_ok=True)

    login_with_cookies(driver, cookie_path)
    scrape_full_profile(driver, profile_url, person_name)

    print("✅ Done. Browser is still open. You can scrape more if needed.")
