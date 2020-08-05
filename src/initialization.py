import json
import src.query

def insert():
    with open("../raw_pokemon_trainer.json", "r") as json_file:
        data = json.load(json_file)
    for pokemon_item in data:
        src.query.pokemon.add(pokemon_item)


if __name__ == '__main__':
    insert()
