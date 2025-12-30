import requests
import json

# 1. DEFINE the Address (URL) and Password (Payload) FIRST
url = "https://web-scraping.dev/api/graphql"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

payload = {
    "query": """
    query GetReviews($first: Int, $after: String) {
      reviews(first: $first, after: $after) {
        edges {
          node {
            id
            text
            rating
            date
          }
        }
      }
    }
    """,
    "variables": {
        "first": 20,
        "after": ""
    }
}

# 2. THEN send the request (using the things we defined above)
response = requests.post(url, json=payload, headers=headers)
print("Status Code:", response.status_code)

# 3. Clean the data
data = response.json()
reviews_raw = data["data"]["reviews"]["edges"]
clean_reviews = []

for item in reviews_raw:
    review = item["node"]  # The actual review is inside 'node'
    clean_reviews.append(review)

# 4. Save to a file
with open("reviews.json", "w") as f:
    json.dump(clean_reviews, f)

print("Success! Scraped", len(clean_reviews), "reviews and saved to reviews.json")