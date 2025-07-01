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


def get_profile_page_source(web_driver, profile_url) -> str:
    """Returns the HTML source of a LinkedIn profile."""
    
    web_driver.get(profile_url)
    time.sleep(5)  # Wait for profile to load
    return web_driver.page_source


def soup_html_parsing(page_source):
    """Parse and save profile data."""
    try:
        soup = BeautifulSoup(page_source, "lxml")  # Fast parser
    except Exception:
        soup = BeautifulSoup(page_source, "html.parser")  # Fallback parser

    profile_data = soup.find("main", {"class": "KvRJXMpQfKwEcgEcBArUUlCAbTXLQvCpWmSxM"})

    if profile_data:
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(str(profile_data))
        print("File saved successfully")
    else:
        print("⚠️ Profile data not found. Possibly wrong class name or not logged in.")


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


def data_preprocessing():
        
    # Read the file content
    with open("profile_data.txt", "r", encoding="utf-8") as file:
        html_content = file.read()

    # Create soup object from the HTML string
    profile_data = BeautifulSoup(html_content, "lxml")  # Or use 'html.parser' if lxml not installed

    # profile_data_text = profile_data.get_text()
    
    # if profile_data_text:
    #     with open("profile_data_text.txt", "w", encoding="utf-8") as file:
    #         file.write(str(profile_data_text))
    #     print("File saved successfully")
    # else:
    #     print("⚠️ Profile data not found. Possibly wrong class name or not logged in.")
    
    sections = profile_data.find_all('section', {'class': 'artdeco-card' })
    
    print(len(sections))
    
    sections_text = [section.get_text() for section in sections]
    
    sections_text = [clean_text(section) for section in sections_text]
    
    sections_text = [remove_duplicates(section) for section in sections_text]
    
    # Convert to list of dicts
    json_data = [{"id": i, "section_text_data": text} for i, text in enumerate(sections_text)]

    # Save to JSON file
    with open("section_text_data.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print("✅ Saved to output.json")
    
    

if __name__ == "__main__":
    aditya_linkedin = "https://www.linkedin.com/in/proaditya/"

    # # Step 1: Sign in
    # signin(driver)

    # # Step 2: Get profile page source
    # page_source = get_profile_page_source(driver, aditya_linkedin)

    # # Step 3: Getting the text from the user profile main html tag
    # soup_html_parsing(page_source)

    data_preprocessing()
    
    # print("✅ Successful execution")
    
