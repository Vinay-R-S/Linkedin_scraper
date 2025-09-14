# 🔍 LinkedIn Profile Scraper (Selenium + BeautifulSoup)

This tool allows you to **scrape complete LinkedIn profiles**, including:

* 🧑 Profile Summary
* 💼 Experience
* 🎓 Education
* 🧾 Certifications
* 📰 Recent Activity

Built using:

* `undetected-chromedriver` (bypass bot detection)
* `selenium` for automation
* `BeautifulSoup` for parsing
* `dotenv` for secure credential management

---

## 🚀 Features

* Stealth login with email/password or saved cookies
* Auto scroll to load dynamic content
* Saves data in clean `JSON` format
* Deduplicates repeated LinkedIn text
* Combines all data into one final JSON
* Easy-to-extend scraping logic

---

## 📦 Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🔐 Setup

1. Create a `.env` file in the root directory:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

2. (Optional) Clear old cookies if needed:

```python
# Uncomment to clear:
# if os.path.exists(cookie_path):
#     os.remove(cookie_path)
```

---

## 💠 How It Works

1. On first run, logs into LinkedIn with your credentials
2. Saves session cookies for future runs
3. Asks for a LinkedIn profile URL
4. Scrapes all key sections
5. Saves the data under `./data/<person_name>/` in multiple JSON files
6. Combines all data into a single `final_profile.json`

---

## 📁 Output Structure

```
data/
└── john-doe/
    ├── profile_text_data.json
    ├── experience_text_data.json
    ├── education_text_data.json
    ├── certifications_text_data.json
    ├── activities_text_data.json
    └── final_profile.json
```

Each file contains structured and cleaned JSON data for use in LLMs, research, or lead generation.

---

## 🧠 Example Usage

```bash
python linkedin_scraper.py
```

You’ll be prompted to enter a LinkedIn profile URL like:

```
🔗 Enter LinkedIn profile URL (or type 'quit' to exit): https://www.linkedin.com/in/john-doe/
```

---

## ⚠️ Disclaimer

This project is for **educational purposes** only. Scraping LinkedIn **violates their Terms of Service**. Use responsibly and at your own risk.

---

## 📌 Notes

* Uses undetected-chromedriver to bypass bot detection
* Supports cookie-based login for faster reuse
* Easily extendable for more profile sections
* Works best with real accounts (dummy accounts may get flagged)

---
