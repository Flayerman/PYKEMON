import json
import urllib.request
import os

POKEMONS_URLS = "pokemongeneration1.json"
TYPES_URLS = "types.json"
TYPES_OUTPUT = "types_sprites"
POKEMONS_OUTPUT = "pokemons_sprites"

def download_images_from_json(json_file_path, output_folder, dl):
    with open(json_file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    
    for item in data:
        if dl == "pokemons":
            url = item['sprite']
        elif dl == "types":
            url = item['image']
        image_name = os.path.basename(item["name"]+".png")
        image_path = os.path.join(output_folder, image_name)
        
        urllib.request.urlretrieve(url, image_path)
        
        if dl == "pokemons":
            url = item['sprite'] = image_path
        elif dl == "types":
            url = item['image'] = image_path
    
    with open(json_file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

download_images_from_json(POKEMONS_URLS, POKEMONS_OUTPUT, "pokemons")
download_images_from_json(TYPES_URLS, TYPES_OUTPUT, "types")
