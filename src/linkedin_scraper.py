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


def signin(web_driver):
    """Sign in to LinkedIn using credentials from environment variables."""
    
    web_driver.get("https://www.linkedin.com/login")
    print("Page Title:", web_driver.title)

    try:
        email = web_driver.find_element(By.ID, "username")
        password = web_driver.find_element(By.ID, "password")

        email.send_keys(os.getenv("EMAIL"))
        password.send_keys(os.getenv("PASSWORD"))

        password.submit()  # Submit the login form
        time.sleep(5)  # Wait for page to load

    except Exception as e:
        print("Login failed:", e)


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

    
def scrape_profile_page(web_driver, profile_url):
    
    web_driver.get(profile_url)
    time.sleep(5)
    
    scroll_logic(web_driver)
    time.sleep(5)
    
    profile_page_source = web_driver.page_source
    
    try:
        soup = BeautifulSoup(profile_page_source, "lxml")  # Fast parser
    except Exception:
        soup = BeautifulSoup(profile_page_source, "html.parser")  # Fallback parser
        
    profile_main = soup.find('main', {'class': 'KvRJXMpQfKwEcgEcBArUUlCAbTXLQvCpWmSxM'})
    
    profile_sections = profile_main.find_all('section', {'class': 'artdeco-card' })
    
    profile_text = [profile_sec.get_text() for profile_sec in profile_sections]
    
    profile_text = [clean_text(pf_text) for pf_text in profile_text]
    
    profile_text = [remove_duplicates(pf_text)  for pf_text in profile_text]
    
    json_data = [{"id": i, "profile_text_data": text} for i, text in enumerate(profile_text)]
    
    # Save to JSON file
    with open("./data/ismail/profile_text_data.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print("✅ Saved to profile_text_data.json")
    

def scrape_recent_activity(web_driver, profile_url):
    
    recent_activity_url = "recent-activity/all/"
    activity_url = profile_url + recent_activity_url

    web_driver.get(activity_url)
    time.sleep(5)
    
    scroll_logic(web_driver)
    time.sleep(5)

    activity_page_source = web_driver.page_source

    try:
        soup = BeautifulSoup(activity_page_source, "lxml")  # Fast parser
    except Exception:
        soup = BeautifulSoup(activity_page_source, "html.parser")  # Fallback parser

    activity_main = soup.find("main", {"class": "KvRJXMpQfKwEcgEcBArUUlCAbTXLQvCpWmSxM"})
    
    activity_divs = activity_main.find_all('div', {'class': 'update-components-text relative update-components-update-v2__commentary'})
    
    activity_text = [act_text.get_text() for act_text in activity_divs]
    
    activity_text = [clean_text(act_text) for act_text in activity_text]
    
    activity_text = [remove_duplicates(act_text) for act_text in activity_text]

    activity_text = activity_text[:20]  # Limit to top 20 posts

    json_data = [{"id": i, "activities_text_data": text} for i, text in enumerate(activity_text)]
    
    # Save to JSON file
    with open("./data/ismail/activities_text_data.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print("✅ Saved to activities_text_data.json")


if __name__ == "__main__":
    
    aditya_linkedin = "https://www.linkedin.com/in/proaditya/"
    
    ismail_linkedin = "https://www.linkedin.com/in/mohammedismail1454/"

    # Step 1: Sign in
    signin(driver)
    
    # Step 2: Scrape profile page -> home page
    scrape_profile_page(driver, ismail_linkedin)
    
    # Step 5: Scrape activites page -> recent-activity page
    scrape_recent_activity(driver, ismail_linkedin)
        
    print("✅ Successful execution")

