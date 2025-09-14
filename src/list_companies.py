import os
import json

base_path = r"E:/SalesBuddy/Linkedin_scraper/data/companies"
companies = []

for company in os.listdir(base_path):
    company_path = os.path.join(base_path, company)
    if os.path.isdir(company_path):
        companies.append({
            "name": company,
            "path": company_path.replace("\\", "/")
        })

print(json.dumps(companies))
