from src.connect import connection
from .insert import insert_to_table, new_query
from pymysql import IntegrityError
from .pokemon import get_pokemon_id
import json


def add(num_pokemon, pokemon):
    for trainer in pokemon["ownedBy"]:
        try:
            num_trainer = get_trainer_id(trainer['name'])
            if num_trainer == -1:
                insert_to_table("trainer", f"'{trainer['name']}', '{trainer['town']}'", " (name, town)")
                num_trainer = get_trainer_id(trainer['name'])

            insert_to_table("owned_by", f"{num_pokemon}, {num_trainer}")

        except IntegrityError as ex:
            print(f"DB Error - {ex}")


def get_trainer_id(trainer):
    try:
        with connection.cursor() as cursor:
            # name, town = trainer.split(' ')
            # query = f"SELECT id FROM trainer WHERE name = '{name}' and town = '{town}';"
            query = f"SELECT id FROM Trainer WHERE name = '{trainer}'"
            cursor.execute(query)
            result = cursor.fetchone()
            return result["id"]

    except Exception:
        return -1


def find_owners(pokemon_name):
    new_query(f"""SELECT T.name
                FROM (SELECT O.trainer_id as id 
                      FROM Pokemon P JOIN Owned_By O on P.id = O.pokemon_id
                      WHERE P.name = '{pokemon_name}') J JOIN Trainer T on T.id = J.id""")


def delete_from_trainer(trainer, pokemon):
    t_id = get_trainer_id(trainer)
    pok_id = get_pokemon_id(pokemon)

    if t_id == -1:
        return json.dumps({"error": "Not Found trainer"}), 404

    if pok_id is None:
        return json.dumps({"error": "Not Found pokemon name"}), 404

    query = f"""DELETE FROM Owned_by \
                WHERE pokemon_id = {pok_id} AND trainer_id = {t_id};"""

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
            return json.dumps({"deleted": f"{pokemon} of {trainer}"}), 200

    except IntegrityError:
        return json.dumps({"internal error": "DB Error"}), 500

    return json.dumps({"ok": "deleted trainer"}), 200