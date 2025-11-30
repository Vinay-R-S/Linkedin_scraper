import os
import json

base_path = r"C:/Users/vinay/OneDrive/Desktop/IS/Zodopt/Linkedin_scraper/data/users"
users = []

if os.path.exists(base_path):
    for user in os.listdir(base_path):
        user_path = os.path.join(base_path, user)
        if os.path.isdir(user_path):
            users.append({
                "name": user,
                "path": user_path.replace("\\", "/")
            })

print(json.dumps(users))
