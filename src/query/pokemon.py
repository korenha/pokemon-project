
# from ..connect import connection
from src.connect import connection
from pymysql import IntegrityError
from .insert import insert_to_table, new_query
from . import trainer, pokemon_type
import json


def add(pokemon):
    try:
        insert_to_table("pokemon",
                        f"""{pokemon['id']}, '{pokemon['name']}', {pokemon['height']}, {pokemon['weight']}""")

    except IntegrityError as ex:
        return json.dumps({"error": "existing pokemon"}), 500

    if "ownedBy" in pokemon.keys():
        trainer.add(pokemon["id"], pokemon)

    pokemon_type.add(pokemon["id"], pokemon["type"])

    return json.dumps({"ok": f"added {pokemon} pokemon"}), 200


def get_pokemon_id(pok_name):
    with connection.cursor() as cursor:
        query = f"SELECT id FROM Pokemon WHERE name = '{pok_name}'"
        cursor.execute(query)
        result = cursor.fetchone()
        connection.commit()
        try:
            return result.get("id")
        except AttributeError:
            return None


def get_heaviest_pokemon():
    query = """SELECT * FROM Pokemon WHERE weight_ = (SELECT MAX(weight_) FROM Pokemon);"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            pokemon = cursor.fetchone()
            if not pokemon:
                return json.dumps({"Error": "pokemon does not exists"}), 404
            return json.dumps(pokemon), 200
    except Exception as ex:
        return {"Error": str(ex)}, 500


def find_pokemon_by_type(type_):
    query = f"""SELECT Pokemon.name \
                FROM Pokemon JOIN Of_type on Pokemon.id = Of_type.pokemon_id \
                WHERE Of_type.type_id = {pokemon_type.get_type_id(type_)} ;"""

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            ans = []
            result = cursor.fetchone()
            while result:
                ans.append(result["name"])
                result = cursor.fetchone()
            return ans, 200

    except IntegrityError as ex:
        return "not found", 404

    except Exception as ex:
        return {"Error": str(ex)}, 500


def find_roster(trainer_name):
    return new_query(f"""SELECT P.name \
                         FROM (SELECT O.pokemon_id as id \
                         FROM Trainer T JOIN Owned_By O on T.id = O.trainer_id \
                         WHERE T.name = '{trainer_name}') J JOIN Pokemon P on P.id = J.id""")
