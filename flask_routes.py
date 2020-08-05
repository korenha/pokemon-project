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

@app.route('/pokemon/trainer/<pok>')
def get_trainer_of_pok(pok):
    ans,error = queries.find_owners(pok)
    return json.dumps({"result":ans}),error

@app.route('/trainer/pokemon/<tra>')
def get_pok_of_trainer(tra):
    ans,error = queries.find_roster(tra)
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


@app.route('/trainer/evolve/<trainer>/<pokemon>', methods=['PATCH'])
def evolve_pokemon(trainer,pokemon):
    t_id = pokemon_insert.get_trainer_id(trainer)
    if not t_id:
        return f"Not Found {trainer}", 404

    if pokemon not in queries.find_roster(trainer):
        return f"{pokemon} isn\'t owned by {trainer}",404

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    pok_details = requests.get(url=url, verify=False)
    try:
        url = pok_details.json()["species"]["url"]
    except Exception as ex:
        return f"Not Found: {pokemon}",404

    url = requests.get(url=url, verify=False).json()["evolution_chain"]["url"]
    details = requests.get(url=url, verify=False).json()
    try:
        evolved_pok = details["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
    except KeyError:
        return f"Can not evolve {pokemon}",300

    url = f"https://pokeapi.co/api/v2/pokemon/{evolved_pok}"

    evolve_pok = requests.get(url=url, verify=False).json()
    query = f"""UPDATE Owned_by 
    SET pokemon_id = {evolve_pok['id']} 
    WHERE trainer_id = {t_id} AND pokemon_id = {pok_details.json()['id']};"""

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return "succeed",200
    except IntegrityError:
        return f"Duplicate entry \'26-24\' for key \'PRIMARY",500


if __name__ == '__main__':
    app.run(port=3001)


