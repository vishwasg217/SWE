import psycopg2
from psycopg2.extras import RealDictCursor
import json

try:
    connection = psycopg2.connect(
        host="localhost",
        database="api_design",
        user="postgres",
        cursor_factory=RealDictCursor
    )

    cursor = connection.cursor()
    print("Connected to the database.")
    
except Exception as e:
    print(f"Error: {e}")

with open("data/the_office/posts.json", "r") as f:
    posts = json.load(f)

for post in posts:
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post["title"], post["content"], post["published"])
    )
    inserted_post = cursor.fetchone()
    connection.commit()
    print(inserted_post)

# cursor.execute("SELECT * FROM posts")
# posts = cursor.fetchall()
# print(posts)
