import requests
import json
import os
import time

# Create folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

url = "https://api.openalex.org/works"

cursor = "*"
page = 1

while True:

    params = {
        "search": "large language models",
        "per-page": 200,
        "cursor": cursor
    }

    response = requests.get(url, params=params)

    data = response.json()

    papers = data["results"]

    if len(papers) == 0:
        break

    filename = f"data/raw/page_{page}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {filename}")

    cursor = data["meta"]["next_cursor"]

    page += 1

    time.sleep(1)