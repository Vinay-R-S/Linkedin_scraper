import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {TAVILY_API_KEY}",
    "Content-Type": "application/json"
}

job_titles = [
    "Head of Sales",
    "Sales Enablement Manager",
    "Revenue Operations Manager",
    "Business Development Lead",
    "Account Executive",
    "Partnerships Manager",
    "Sales Development Representative (SDR)",
    "Inside Sales Manager",
    "Enterprise Sales Head",
    "VP of Sales"
]

locations = [
    "India",
    "USA",
    "UK",
    "Canada",
    "Australia",
    "UAE",
    "Singapore"
]

roles = [
    "Sales",
    "Business Development",
    "Revenue Operations",
    "Go-to-Market",
    "Partnerships",
    "Growth"
]

def tavily_search(query):
    payload = {
        "query": query,
        "include_answer": False,
        "search_depth": "advanced",
        "max_results": 10
    }
    response = requests.post("https://api.tavily.com/search", headers=HEADERS, json=payload)
    return response.json()

def extract_name(title_str):
    # Very basic name extractor using title field
    match = re.search(r'^(.*?)(?=\s+-\s+| at | \|)', title_str)
    return match.group(0).strip() if match else "Unknown"

def generate_leads():
    all_leads = []
    for title in job_titles:
        for loc in locations:
            # Try 3 types of queries to maximize result quality
            queries = [
                f'{title} at B2B SaaS companies in {loc} site:linkedin.com/in/',
                f'{title} contact info in {loc} B2B SaaS site:crunchbase.com OR site:rocketreach.co OR site:zoominfo.com',
                f'"{title}" in "{loc}" profile OR bio OR team site:*.com -site:linkedin.com'
            ]

            for search_query in queries:
                print(f"🔍 Searching: {search_query}")
                results = tavily_search(search_query)

                for res in results.get("results", []):
                    
                    name = extract_name(res.get("title", ""))
                    url = res.get("url", "")
                    content = res.get("content", "")

                    lead = {
                        "name": name,
                        "company": None,
                        "role": title,
                        "email_id": None,
                        "number": None,
                        "experience": None,
                        "qualifications": None,
                        "location": loc,
                        "linkedin_url": url if "linkedin.com/in" in url else None,
                        "source_url": url,
                        "a_detailed_info_that_person": content.strip()
                    }

                    all_leads.append(lead)

    return all_leads

def save_to_json(data, filename="leads_1.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Leads saved to {filename}")

# Run the script
if __name__ == "__main__":
    leads = generate_leads()
    save_to_json(leads)
