from flask import Flask, Response
import requests
import query
import json
# from .connect import connection
# from pymysql import IntegrityError


app = Flask(__name__)


@app.route('/types/<pokemon>', methods=['PATCH'])
def update_type(pokemon):
    res = requests.get(url=f"https://pokeapi.co/api/v2/pokemon/{pokemon}", verify=False)
    query.pokemon_type.add(query.pokemon.get_pokemon_id(pokemon),
                           [type_['type']['name'] for type_ in res.json()["types"]])
    return Response("update")


@app.route('/pokemon/<pokemon>', methods=['POST'])
def add_pokemon(pokemon):
    res = requests.get(url=f"https://pokeapi.co/api/v2/pokemon/{pokemon}", verify=False).json()
    return query.pokemon.add({"id": res["id"],
                              "name": pokemon,
                              "type": [type_['type']['name'] for type_ in res["types"]],
                              "height": res["height"],
                              "weight": res["weight"]
                              })


@app.route('/types/<type_>')
def get_pokemon_by_type(type_):
    ans, error = query.pokemon.find_pokemon_by_type(type_)
    return json.dumps({"result": ans})


@app.route('/trainer/<pokemon>')
def get_trainer_of_pokemon(pokemon):
    ans, error = query.trainer.find_owners(pokemon)
    return json.dumps({"result": ans}), error


@app.route('/pokemon/<trainer>')
def get_pokemon_of_trainer(trainer):
    ans, error = query.pokemon.find_roster(trainer)
    return json.dumps({"result": ans}), error


@app.route('/trainer/<trainer>/<pokemon>', methods=['DELETE'])
def delete_from_trainer(trainer, pokemon):
    return query.trainer.delete_from_trainer(trainer, pokemon)


# @app.route('/trainer/evolve/<trainer>/<pokemon>', methods=['PATCH'])
# def evolve_pokemon(trainer,pokemon):
#     t_id = get.get_trainer_id(trainer)
#     if not t_id:
#         return f"Not Found {trainer}", 404
#
#     if pokemon not in queries.find_roster(trainer):
#         return f"{pokemon} isn\'t owned by {trainer}",404
#
#     url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
#     pok_details = requests.get(url=url, verify=False)
#     try:
#         url = pok_details.json()["species"]["url"]
#     except Exception as ex:
#         return f"Not Found: {pokemon}",404
#
#     url = requests.get(url=url, verify=False).json()["evolution_chain"]["url"]
#     details = requests.get(url=url, verify=False).json()
#     try:
#         evolved_pok = details["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
#     except KeyError:
#         return f"Can not evolve {pokemon}",300
#
#     url = f"https://pokeapi.co/api/v2/pokemon/{evolved_pok}"
#
#     evolve_pok = requests.get(url=url, verify=False).json()
#     query = f"""UPDATE Owned_by
#     SET pokemon_id = {evolve_pok['id']}
#     WHERE trainer_id = {t_id} AND pokemon_id = {pok_details.json()['id']};"""
#
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             connection.commit()
#             return "succeed",200
#     except IntegrityError:
#         return f"Duplicate entry \'26-24\' for key \'PRIMARY",500


if __name__ == '__main__':
    app.run(port=3001)


