import json
import requests

URL = "https://pokebuildapi.fr/api/v1/"

slug = ["pokemon/generation/1", "types"]

for s in slug:
    response = requests.get(URL + s)
    data = response.json()

    with open(f"{s.replace('/', '')}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

    
