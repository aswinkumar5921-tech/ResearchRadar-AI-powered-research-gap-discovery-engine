import requests

url = "https://api.openalex.org/works"

params = {
    "search": "large language models",
    "per-page": 5
}

response = requests.get(url, params=params)

data = response.json()

for paper in data["results"]:
    print("=" * 50)
    print("Title:", paper["title"])
    print("Year:", paper["publication_year"])
    print("OpenAlex ID:", paper["id"])
    
import json

print(json.dumps(data["results"][0], indent=2))