import os
import time
import re
import json
import pickle
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Load .env
load_dotenv(override=True)
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Setup Chrome with stealth
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

try:
    driver = uc.Chrome(options=chrome_options, headless=False)
    print("Chrome driver initialized successfully!")
except Exception as e:
    print(f"Failed to initialize driver: {e}")
    exit(1)

main_class_code = "utrLhBqOdLacwtLYWCbvaTqJwYxMYcARs"
section_class_code = "artdeco-card pv-profile-card break-words mt2"
contact_class_code = "artdeco-modal artdeco-modal--layer-default"
contact_div_class_code = "artdeco-modal__content ember-view"

experience_section_class_code = "artdeco-card pb3"
education_section_class_code = "artdeco-card pb3"
activity_section_class_code = "artdeco-card pb3"
certification_section_class_code = "artdeco-card pb3"
profile_section_class_code = "artdeco-card pv-profile-card break-words mt2"


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

def scroll_logic(web_driver, max_posts=20, activity=False):
    last_height = web_driver.execute_script("return document.body.scrollHeight")
    seen_posts = set()
    for _ in range(15):
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        if activity:
            soup = BeautifulSoup(web_driver.page_source, "lxml")
            posts = soup.find_all("div", {"class": "update-components-text relative update-components-update-v2__commentary"})
            seen_posts.update(posts)
            if len(seen_posts) >= max_posts:
                print(f"Loaded {len(seen_posts)} posts. Stopping scroll.")
                break
        new_height = web_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def auto_login(driver):
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(5)
    if "feed" in driver.current_url:
        print("Already logged in.")
        return True
    
    print("Manual login required. Opening LinkedIn...")
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)
    input("Please complete login manually, then press ENTER here...")
    
    if "feed" in driver.current_url:
        print("Logged in manually.")
        return True
    else:
        print("Login failed even after manual attempt.")
        return False

def generic_scraper(web_driver, url, main_div_class, content_div_class, output_key_name, output_filename, limit=20):
    web_driver.get(url)
    time.sleep(5)
    scroll_logic(web_driver, max_posts=limit if output_key_name == "activities_text_data" else 0, activity=(output_key_name == "activities_text_data"))
    time.sleep(5)
    try:
        soup = BeautifulSoup(web_driver.page_source, "lxml")
    except Exception:
        soup = BeautifulSoup(web_driver.page_source, "html.parser")
    main_div = soup.find("div", {"class": main_div_class}) or soup.find("main", {"class": main_div_class})
    content_divs = main_div.find_all("div", {"class": content_div_class}) if main_div else []
    if limit:
        content_divs = content_divs[:limit]
    text_data = [remove_duplicates(clean_text(div.get_text())) for div in content_divs]
    json_data = [{"id": i, output_key_name: text} for i, text in enumerate(text_data)]
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print(f"Saved to {output_filename}")
    return json_data

def scrape_profile_page(web_driver, profile_url, person_name):
    web_driver.get(profile_url)
    time.sleep(5)
    scroll_logic(web_driver)
    time.sleep(5)
    soup = BeautifulSoup(web_driver.page_source, "lxml")
    profile_main = soup.find("main", {"class": main_class_code})
    profile_sections = profile_main.find_all("section", {"class": profile_section_class_code}) if profile_main else []
    text_data = [remove_duplicates(clean_text(sec.get_text())) for sec in profile_sections]
    json_data = [{"id": i, "profile_text_data": text} for i, text in enumerate(text_data)]
    with open(f"./data/users/{person_name}/profile_text_data.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print("Saved profile_text_data.json")
    return json_data

def scrape_experience(driver, url, name):
    return generic_scraper(driver, url + "details/experience/", main_class_code,
                           experience_section_class_code, "experience_text_data", f"./data/users/{name}/experience_text_data.json")

def scrape_education(driver, url, name):
    return generic_scraper(driver, url + "details/education/", main_class_code,
                           education_section_class_code, "education_text_data", f"./data/users/{name}/education_text_data.json")

def scrape_certifications(driver, url, name):
    return generic_scraper(driver, url + "details/certifications/", main_class_code,
                           certification_section_class_code, "certifications_text_data", f"./data/users/{name}/certifications_text_data.json")

def scrape_recent_activity(driver, url, name):
    return generic_scraper(driver, url + "recent-activity/all/", main_class_code,
                           activity_section_class_code,
                           "activities_text_data", f"./data/users/{name}/activities_text_data.json", limit=15)

def scrape_contact_info(driver, url, name):
    return generic_scraper(driver, url + "overlay/contact-info/", contact_class_code,
                           contact_div_class_code, 
                           "contact_data", f"./data/users/{name}/contact.json")

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
    with open(f"./data/users/{person_name}/final_profile.json", "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4, ensure_ascii=False)
    print("All data combined")

def scrape_full_profile(driver, profile_url, person_name="LinkedIn-profile"):
    os.makedirs(f"./data/users/{person_name}", exist_ok=True)
    profile_data = scrape_profile_page(driver, profile_url, person_name)
    experience_data = scrape_experience(driver, profile_url, person_name)
    education_data = scrape_education(driver, profile_url, person_name)
    cert_data = scrape_certifications(driver, profile_url, person_name)
    activity_data = scrape_recent_activity(driver, profile_url, person_name)
    contact_data = scrape_contact_info(driver, profile_url, person_name)
    combine_all_data(person_name, profile_data, experience_data, education_data, cert_data, activity_data, contact_data)

if __name__ == "__main__":
    if auto_login(driver):
        try:
            while True:
                print("\nWhat do you want to scrape?")
                print("Person Profile")
                choice = input("Enter your choice (1 to scrape person profile, or type 'quit' to exit): ").strip()
                if choice.lower() == "quit":
                    print("Exiting...")
                    break
                if choice == "1":
                    profile_url = input("\nEnter LinkedIn profile URL: ").strip()
                    person_name = profile_url.rstrip('/').split("/")[-1]
                    scrape_full_profile(driver, profile_url, person_name)
                else:
                    print("Invalid choice. Please enter 1.")
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            if driver:
                try:
                    print("Closing browser properly...")
                    driver.quit()
                except Exception as e:
                    print(f"Error closing browser: {e}")
