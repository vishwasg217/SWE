import requests
import json

from app.schemas import UserCreate

with open("data/the_office/users.json", "r") as f:
    users = json.load(f)

# user = UserCreate(**users[0])
# print(user)

for user in users:
    response = requests.post("http://127.0.0.1:8000/users", json=user)
    if response.status_code != 201:
        print(f"Failed to create user: {user}")
    else:
        print(response.json())
