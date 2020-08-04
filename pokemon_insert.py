import pymysql
from pymysql import IntegrityError
import json


connection = pymysql.connect(
    host="localhost",
    user="DELL",
    password="",
    db="pokemon_data",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


if connection.open:
    print("the connection is opened")


def get_num_trainer(name, town):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT id FROM trainer WHERE name = '{name}' and town = '{town}';"
            cursor.execute(query)
            result = cursor.fetchone()
            return result["id"]

    except Exception as ex:
        return -1


def insert_into_table(name_table, values, fields=""):
    try:
        with connection.cursor() as cursor:
            query = f"INSERT into {name_table}{fields} values ({values});"
            cursor.execute(query)
            connection.commit()

    except IntegrityError as ex:
        print(f"DB Error - {ex}")


def insert_into_owned_by_and_trainer(num_pokemon, pokemon):
    for trainer in pokemon["ownedBy"]:
        num_trainer = get_num_trainer(trainer['name'], trainer['town'])
        if num_trainer == -1:
            insert_into_table("trainer", f"'{trainer['name']}', '{trainer['town']}'", " (name, town)")
            num_trainer = get_num_trainer(trainer['name'], trainer['town'])

        insert_into_table("owned_by", f"'{num_pokemon + 1}', '{num_trainer}'")


def get_num_pokemon(type_):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT id FROM types WHERE name = '{type_}';"
            cursor.execute(query)
            result = cursor.fetchone()
            return result["id"]

    except Exception as ex:
        return -1


def insert_into_of_type_and_types(num_pokemon, pokemon):
    # for type_ in pokemon["type"]:
    num_trainer = get_num_pokemon(pokemon["type"])
    if num_trainer == -1:
        insert_into_table("types", f"'{pokemon['type']}'", " (name)")
        num_trainer = get_num_pokemon(pokemon['type'])
        insert_into_table("of_type", f"{num_pokemon + 1}, {num_trainer}")

    else:
        insert_into_table("of_type", f"{num_pokemon + 1}, {num_trainer}")


def insert():
    with open("raw_pokemon_trainer.json") as file:
        pokemons = json.load(file)

    for num_pokemon, pokemon in enumerate(pokemons):
        insert_into_table("pokemon",
                          f"{pokemon['id']}, '{pokemon['name']}', "
                          f"{pokemon['height']}, {pokemon['weight']}")

        insert_into_owned_by_and_trainer(num_pokemon, pokemon)

        insert_into_of_type_and_types(num_pokemon, pokemon)


if __name__ == '__main__':
    insert()
