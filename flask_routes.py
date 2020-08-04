from flask import Flask
import requests
from certifi import where
import pokemon_insert
from pokemon_insert import get_pokeon_id,insert_to_table,get_type_id
import queries
app = Flask(__name__)
print(where())

@app.route('/types/<pokemon>', methods=['PATCH'])
def update_type(pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    res = requests.get(url=url, verify=False)

    for type_ in res.json()["types"]:
        if not get_type_id(type_['type']['name']):
            insert_to_table("Type",f"'{type_['type']['name']}'","name")
        insert_to_table("Of_type",f"{get_pokeon_id(pokemon)},{get_type_id(type_['type']['name'])}","pokemon_id,type_id")

@app.route('/pokemon/<pokemon>', methods=['PUT'])
def add_pok(pokemon_details):
    pokemon_insert.add_pokemon(pokemon_details)
    pokemon_insert.add_to_of_type(pokemon_details['id'],pokemon_details['types'])

@app.route('/types/<pokemon>')
def get_by_type(type):
    queries.find_by_type(type)


update_type("vileplume")
add_pok({"id":10100,
        "name": "raichu-alola",
        "height": 7,
         "weight": 210,
         "types": ["electric","psychic"]
         })

