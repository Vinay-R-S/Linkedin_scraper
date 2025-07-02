import os
import time
import warnings
import re
import json
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


# def signin(web_driver):
#     """Sign in to LinkedIn using credentials from environment variables."""
    
#     web_driver.get("https://www.linkedin.com/login")
#     print("Page Title:", web_driver.title)

#     try:
#         email = web_driver.find_element(By.ID, "username")
#         password = web_driver.find_element(By.ID, "password")

#         email.send_keys(os.getenv("EMAIL"))
#         password.send_keys(os.getenv("PASSWORD"))

#         password.submit()  # Submit the login form
#         time.sleep(5)  # Wait for page to load

#     except Exception as e:
#         print("Login failed:", e)

def manual_signin(web_driver):
    """Manually sign in to LinkedIn, then wait for user to type 'start' to proceed."""
    web_driver.get("https://www.linkedin.com/login")
    print("🔐 Please login manually in the browser...")

    # Wait for user input to continue
    while True:
        user_input = input("⏳ Type 'start' after you complete login and verification: ").strip().lower()
        if user_input == "start":
            print("✅ Login confirmed. Proceeding with scraping...")
            break
        else:
            print("❗ Invalid input. Type 'start' to begin scraping.")



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
     # Scroll logic added to load more posts
    last_height = web_driver.execute_script("return document.body.scrollHeight")
    for _ in range(15):
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = web_driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    
# def scrape_profile_page(web_driver, profile_url):
    
#     web_driver.get(profile_url)
#     time.sleep(5)
    
#     scroll_logic(web_driver)
#     time.sleep(5)
    
#     profile_page_source = web_driver.page_source
    
#     try:
#         soup = BeautifulSoup(profile_page_source, "lxml")  # Fast parser
#     except Exception:
#         soup = BeautifulSoup(profile_page_source, "html.parser")  # Fallback parser
        
#     profile_main = soup.find('main', {'class': 'KvRJXMpQfKwEcgEcBArUUlCAbTXLQvCpWmSxM'})
    
#     profile_sections = profile_main.find_all('section', {'class': 'artdeco-card' })
    
#     profile_text = [profile_sec.get_text() for profile_sec in profile_sections]
    
#     profile_text = [clean_text(pf_text) for pf_text in profile_text]
    
#     profile_text = [remove_duplicates(pf_text)  for pf_text in profile_text]
    
#     json_data = [{"id": i, "profile_text_data": text} for i, text in enumerate(profile_text)]
    
#     # Save to JSON file
#     with open("./data/taufeeq/profile_text_data.json", "w", encoding="utf-8") as f:
#         json.dump(json_data, f, indent=4, ensure_ascii=False)

#     print("✅ Saved to profile_text_data.json")
    

# def scrape_recent_activity(web_driver, profile_url):
    
#     recent_activity_url = "recent-activity/all/"
#     activity_url = profile_url + recent_activity_url

#     web_driver.get(activity_url)
#     time.sleep(5)
    
#     scroll_logic(web_driver)
#     time.sleep(5)

#     activity_page_source = web_driver.page_source

#     try:
#         soup = BeautifulSoup(activity_page_source, "lxml")  # Fast parser
#     except Exception:
#         soup = BeautifulSoup(activity_page_source, "html.parser")  # Fallback parser

#     activity_main = soup.find("main", {"class": "KvRJXMpQfKwEcgEcBArUUlCAbTXLQvCpWmSxM"})
    
#     activity_divs = activity_main.find_all('div', {'class': 'update-components-text relative update-components-update-v2__commentary'})
    
#     activity_text = [act_text.get_text() for act_text in activity_divs]
    
#     activity_text = [clean_text(act_text) for act_text in activity_text]
    
#     activity_text = [remove_duplicates(act_text) for act_text in activity_text]

#     activity_text = activity_text[:20]  # Limit to top 20 posts

#     json_data = [{"id": i, "activities_text_data": text} for i, text in enumerate(activity_text)]
    
#     # Save to JSON file
#     with open("./data/taufeeq/activities_text_data.json", "w", encoding="utf-8") as f:
#         json.dump(json_data, f, indent=4, ensure_ascii=False)

#     print("✅ Saved to activities_text_data.json")


# def scrape_experience(web_driver, profile_url):
#     detailed_experience_url = "details/experience/"
#     experience_url = profile_url + detailed_experience_url

#     web_driver.get(experience_url)
#     time.sleep(5)
    
#     scroll_logic(web_driver)
#     time.sleep(5)

#     experience_page_source = web_driver.page_source

#     try:
#         soup = BeautifulSoup(experience_page_source, "lxml")  # Fast parser
#     except Exception:
#         soup = BeautifulSoup(experience_page_source, "html.parser")  # Fallback parser'
        
#     # scaffold-finite-scroll__content -> class for main div
#     # LWlsiCwfBojCMKjczOoYFrNXHLWLZQzJZPw hXSIBQFiZpUIAllWMsrCQfCDXgDjwnBGodc BOWvRyXFbKrnuISjECjeIPpaGdtYghySFZyeA -> classes for exp div's

#     experience_main_div = soup.find("div", {"class": "scaffold-finite-scroll__content"})
    
#     experience_divs = experience_main_div.find_all('div', {'class': 'LWlsiCwfBojCMKjczOoYFrNXHLWLZQzJZPw hXSIBQFiZpUIAllWMsrCQfCDXgDjwnBGodc BOWvRyXFbKrnuISjECjeIPpaGdtYghySFZyeA'})
    
#     experience_text = [exp_text.get_text() for exp_text in experience_divs]
    
#     experience_text = [clean_text(exp_text) for exp_text in experience_text]
    
#     experience_text = [remove_duplicates(exp_text) for exp_text in experience_text]

#     # experience_text = experience_text[:20]  # Limit to top 20 posts

#     json_data = [{"id": i, "experience_text_data": text} for i, text in enumerate(experience_text)]
    
#     # Save to JSON file
#     with open("./data/taufeeq/experience_text_data.json", "w", encoding="utf-8") as f:
#         json.dump(json_data, f, indent=4, ensure_ascii=False)

#     print("✅ Saved to experience_text_data.json")
    

# def scrape_education(web_driver, profile_url):
#     detailed_education_url = "details/education/"
#     education_url = profile_url + detailed_education_url

#     web_driver.get(education_url)
#     time.sleep(5)
    
#     scroll_logic(web_driver)
#     time.sleep(5)

#     education_page_source = web_driver.page_source

#     try:
#         soup = BeautifulSoup(education_page_source, "lxml")  # Fast parser
#     except Exception:
#         soup = BeautifulSoup(education_page_source, "html.parser")  # Fallback parser'
        
#     # scaffold-finite-scroll__content -> class for main div
#     # LWlsiCwfBojCMKjczOoYFrNXHLWLZQzJZPw hXSIBQFiZpUIAllWMsrCQfCDXgDjwnBGodc BOWvRyXFbKrnuISjECjeIPpaGdtYghySFZyeA -> classes for exp div's

#     education_main_div = soup.find("div", {"class": "scaffold-finite-scroll__content"})
    
#     education_divs = education_main_div.find_all('div', {'class': 'LWlsiCwfBojCMKjczOoYFrNXHLWLZQzJZPw hXSIBQFiZpUIAllWMsrCQfCDXgDjwnBGodc BOWvRyXFbKrnuISjECjeIPpaGdtYghySFZyeA'})
    
#     education_text = [edu_text.get_text() for edu_text in education_divs]
    
#     education_text = [clean_text(edu_text) for edu_text in education_text]
    
#     education_text = [remove_duplicates(edu_text) for edu_text in education_text]

#     # education_text = education_text[:20]  # Limit to top 20 posts

#     json_data = [{"id": i, "education_text_data": text} for i, text in enumerate(education_text)]
    
#     # Save to JSON file
#     with open("./data/taufeeq/education_text_data.json", "w", encoding="utf-8") as f:
#         json.dump(json_data, f, indent=4, ensure_ascii=False)

#     print("✅ Saved to education_text_data.json")


# def scrape_certifications(web_driver, profile_url):
#     detailed_certifications_url = "details/certifications/"
#     certifications_url = profile_url + detailed_certifications_url

#     web_driver.get(certifications_url)
#     time.sleep(5)
    
#     scroll_logic(web_driver)
#     time.sleep(5)

#     certifications_page_source = web_driver.page_source

#     try:
#         soup = BeautifulSoup(certifications_page_source, "lxml")  # Fast parser
#     except Exception:
#         soup = BeautifulSoup(certifications_page_source, "html.parser")  # Fallback parser'
        
#     # scaffold-finite-scroll__content -> class for main div
#     # LWlsiCwfBojCMKjczOoYFrNXHLWLZQzJZPw hXSIBQFiZpUIAllWMsrCQfCDXgDjwnBGodc BOWvRyXFbKrnuISjECjeIPpaGdtYghySFZyeA -> classes for exp div's

#     certifications_main_div = soup.find("div", {"class": "scaffold-finite-scroll__content"})
    
#     certifications_divs = certifications_main_div.find_all('div', {'class': 'LWlsiCwfBojCMKjczOoYFrNXHLWLZQzJZPw hXSIBQFiZpUIAllWMsrCQfCDXgDjwnBGodc BOWvRyXFbKrnuISjECjeIPpaGdtYghySFZyeA'})
    
#     certifications_text = [certificate_text.get_text() for certificate_text in certifications_divs]
    
#     certifications_text = [clean_text(certificate_text) for certificate_text in certifications_text]
    
#     certifications_text = [remove_duplicates(certificate_text) for certificate_text in certifications_text]

#     # certifications_text = certifications_text[:20]  # Limit to top 20 posts

#     json_data = [{"id": i, "certifications_text_data": text} for i, text in enumerate(certifications_text)]
    
#     # Save to JSON file
#     with open("./data/taufeeq/certifications_text_data.json", "w", encoding="utf-8") as f:
#         json.dump(json_data, f, indent=4, ensure_ascii=False)

#     print("✅ Saved to certifications_text_data.json")


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

    json_data = [{ "id": i, output_key_name: text } for i, text in enumerate(text_data)]

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Saved to {output_filename}")
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

    # Save final combined file
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
    
    # person = "taufeeq"
    # aditya_linkedin = "https://www.linkedin.com/in/proaditya/"
    # ismail_linkedin = "https://www.linkedin.com/in/mohammedismail1454/"
    
    
    # # Step 1: Sign in
    # signin(driver)
    
    # # Step 2: Scrape profile page -> home page
    # scrape_profile_page(driver, ismail_linkedin)
    
    # # Step 5: Scrape activites page -> recent-activity page
    # scrape_recent_activity(driver, ismail_linkedin)
    
    profile_url = "https://www.linkedin.com/in/taufeeq/"
    person_name = "Taufeeq"
    
    # Step 1: Sign in
    # signin(driver)
    
    manual_signin()
    
    time.sleep(10)
    
    scrape_full_profile(driver, profile_url, person_name)
    
        
    print("✅ Successful execution")