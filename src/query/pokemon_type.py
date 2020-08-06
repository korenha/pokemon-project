from src.connect import connection
from .insert import insert_to_table
from pymysql import IntegrityError
from .api_pokemons import get_pokemon_details
from . import pokemon
import json


def insert(num_pokemon, type_):
    try:
        num_type = get_type_id(type_)

        if num_type == -1:
            insert_to_table("types", f"'{type_}'", " (name)")
            num_type = get_type_id(type_)

        insert_to_table("of_type", f"{num_pokemon}, {num_type}")
        return "insert"

    except IntegrityError as ex:
        return "exist"


def add(num_pokemon, type_):
    if isinstance(type_, list):
        count = 0
        for item in type_:
            if insert(num_pokemon, item) != "exist":
                count += 1

        if count == len(type_):
            return "error"

    else:
        insert(num_pokemon, type_)


def get_type_id(type_):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT id FROM Types WHERE name = '{type_}';"
            cursor.execute(query)
            result = cursor.fetchone()
            connection.commit()
            return result["id"]

    except Exception:
        return -1


def update(pokemon_):
    try:
        res = get_pokemon_details(pokemon_)
        if add(pokemon.get_pokemon_id(pokemon_),
               [type_['type']['name'] for type_ in res["types"]]) == 'error':
            return json.dumps({"error": "the types are update"}), 400
        return json.dumps({"ok": "update"}), 200

    except Exception:
        return json.dumps({"error": "there is no such pokemon"}), 400
