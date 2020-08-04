from flask import Flask
import requests
from certifi import where
import pokemon_insert
from pokemon_insert import get_pokeon_id,insert_to_table,get_type_id
import queries
import json
from pokemon_insert import connection
from pymysql import IntegrityError

app = Flask(__name__)
# print(where())

@app.route('/types/<pokemon>', methods=['PATCH'])
def update_type(pokemon):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    res = requests.get(url=url, verify=False)
    for type_ in res.json()["types"]:
        if not get_type_id(type_['type']['name']):
            insert_to_table("Type",f"'{type_['type']['name']}'","name")
        insert_to_table("Of_type",f"{get_pokeon_id(pokemon)},{get_type_id(type_['type']['name'])}","pokemon_id,type_id")

@app.route('/pokemon/<pokemon>', methods=['POST'])
def add_pok(pokemon):
    pokemon_insert.add_pokemon(pokemon)
    pokemon_insert.add_to_of_type(pokemon['id'],pokemon['types'])

@app.route('/types/<type>')
def get_by_type(type):
    ans,error = queries.find_by_type(type)
    return json.dumps({"result":ans}),error

@app.route('/trainer/<trainer>/<pokemon>', methods=['DELETE'])
def delete_from_trainer(trainer,pokemon):
    t_id = pokemon_insert.get_trainer_id(trainer)
    pok_id = pokemon_insert.get_pokeon_id(pokemon)
    query = f"DELETE FROM Owned_by\
            WHERE pokemon_id = {pok_id} AND trainer_id = {t_id};"
    if not t_id or not pok_id:
        return "Not Found",404
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return json.dumps({"deleted":f"{pokemon} of {trainer}"}),200
    except IntegrityError:
        return "Not Found",404


# update_type("vileplume")
# add_pok({"id":10100,
#         "name": "raichu-alola",
#         "height": 7,
#          "weight": 210,
#          "types": ["electric","psychic"]
#          })

# print(get_by_type("grass"))


if __name__ == '__main__':
    app.run(port=3001)


