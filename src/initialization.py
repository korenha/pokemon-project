import pymysql
from pymysql import IntegrityError
import json
from query import get,post

def insert():
    with open("raw_pokemon_trainer.json", "r") as json_file:
        data = json.load(json_file)
    types_set = {raw["type"] for raw in data}
    for type in types_set:
        post.insert_to_table("Types", f"'{type}'", "name")
    for raw in data:
        post.add_pokemon(raw)
        post.add_to_of_type(raw['id'], [raw['type']])
        for trainer in raw["ownedBy"]:
            try:
                post.insert_to_table("Trainer", f"'{trainer['name']}','{trainer['town']}'", "name,town")
            except IntegrityError:
                pass
            post.insert_to_table("Owned_by", f"{raw['id']},{get.get_trainer_id(trainer['name'])}", "pokemon_id,trainer_id")

if __name__ == '__main__':
    insert()
