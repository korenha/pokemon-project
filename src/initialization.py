import json
import models

def insert():
    with open("../raw_pokemon_trainer.json", "r") as json_file:
        data = json.load(json_file)
    for pokemon_item in data:
        models.pokemon.add(pokemon_item)


if __name__ == '__main__':
    insert()
