import requests
import json

from app.schemas import UserCreate

with open("data/the_office/posts.json", "r") as f:
    posts = json.load(f)

# user = UserCreate(**users[0])
# print(user)

for post in posts:
    response = requests.post(
        url="http://127.0.0.1:8000/posts",
        json=post,
    )
    if response.status_code != 201:
        print(f"Failed to create post: {post}")
    else:
        print(response.json())