import pymysql
from pymysql import IntegrityError
import json

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1",
    db="pokemon_data",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


# def get_num_trainer(name, town):
#     try:
#         with connection.cursor() as cursor:
#             query = f"SELECT id FROM trainer WHERE name = '{name}' and town = '{town}';"
#             cursor.execute(query)
#             result = cursor.fetchone()
#             return result["id"]
#
#     except Exception:
#         return -1
#
#
# def insert_into_table(name_table, values, fields=""):
#     try:
#         with connection.cursor() as cursor:
#             query = f"INSERT into {name_table}{fields} values ({values});"
#             cursor.execute(query)
#             connection.commit()
#
#     except IntegrityError as ex:
#         print(f"DB Error - {ex}", values)
#
#
# def insert_into_owned_by_and_trainer(num_pokemon, pokemon):
#     for trainer in pokemon["ownedBy"]:
#         num_trainer = get_num_trainer(trainer['name'], trainer['town'])
#         if num_trainer == -1:
#             insert_into_table("trainer", f"'{trainer['name']}', '{trainer['town']}'", " (name, town)")
#             num_trainer = get_num_trainer(trainer['name'], trainer['town'])
#
#         insert_into_table("owned_by", f"'{num_pokemon + 1}', '{num_trainer}'")
#
#
# def get_id_type(type_):
#     try:
#         with connection.cursor() as cursor:
#             query = f"SELECT id FROM types WHERE name = '{type_}';"
#             cursor.execute(query)
#             result = cursor.fetchone()
#             return result["id"]
#
#     except Exception:
#         return -1
#
#
# def insert_into_of_type_and_types(num_pokemon, type_):
#     num_trainer = get_id_type(type_)
#     if num_trainer == -1:
#         insert_into_table("types", f"'{type_}'", " (name)")
#         num_trainer = get_id_type(type_)
#         insert_into_table("of_type", f"{num_pokemon + 1}, {num_trainer}")
#
#     else:
#         insert_into_table("of_type", f"{num_pokemon + 1}, {num_trainer}")
#
#
# def insert_pokemon(pokemon):
#     # insert_into_table("pokemon",
#     #                   f"""{pokemon['id']}, '{pokemon['name']}',
#     #                   {pokemon['height']}, {pokemon['weight']}""")
#
#     if isinstance(pokemon["type"], list):
#         for type_ in pokemon["type"]:
#             insert_into_of_type_and_types(pokemon["id"], type_)
#     else:
#         insert_into_of_type_and_types(pokemon["id"], pokemon["type"])
#
#     # insert_into_owned_by_and_trainer(pokemon["id"], pokemon)
#
# def insert():
#     with open("raw_pokemon_trainer.json") as file:
#         pokemons = json.load(file)
#
#     for pokemon in pokemons:
#         insert_pokemon(pokemon)
#
#
# if __name__ == '__main__':
#     if connection.open:
#         print("the connection is opened")
#     insert()
def add_pokemon(pok):
    insert_to_table("Pokemon", f"{pok['id']},'{pok['name']}',{pok['height']},{pok['weight']}", "id,name,height,weight")


def get_pokeon_id(pok_name):
    with connection.cursor() as cursor:
        query = f"SELECT id FROM Pokemon WHERE name = '{pok_name}'"
        cursor.execute(query)
        result = cursor.fetchone()
        connection.commit()
        try:
            return result.get("id")
        except AttributeError:
            return None

def get_trainer_id(trainer):
    with connection.cursor() as cursor:
        query = f"SELECT id FROM Trainer WHERE name = '{trainer['name']}' && town = '{trainer['town']}'"
        cursor.execute(query)
        result = cursor.fetchone()
        connection.commit()
        try:
            return result.get("id")
        except AttributeError:
            return None
def insert_to_table(table,values,fields=""):
    try:
        with connection.cursor() as cursor:
            query = f"INSERT into {table} ({fields}) values({values})"
            cursor.execute(query)
            connection.commit()
            print (f"succeed insert {values} into {table}")
    except IntegrityError:
        print ("existed")

def get_type_id(type):
    with connection.cursor() as cursor:
        query = f"SELECT id FROM Types WHERE name = '{type}';"
        cursor.execute(query)
        result = cursor.fetchone()
        connection.commit()
        try:
            return result.get("id")
        except AttributeError:
            return None

def add_to_of_type(pok_id,types):
    for type in types:
        insert_to_table("Of_type",f"{pok_id},{get_type_id(type)}","pokemon_id,type_id")


def insert():
    with open("raw_pokemon_trainer.json", "r") as json_file:
        data = json.load(json_file)
    types_set = {raw["type"] for raw in data}
    for type in types_set:
        insert_to_table("Types",f"'{type}'","name")
    for raw in data:
        add_pokemon(raw)
        add_to_of_type(raw['id'],[raw['type']])
        for trainer in raw["ownedBy"]:
            try:
                insert_to_table("Trainer", f"'{trainer['name']}','{trainer['town']}'", "name,town")
            except IntegrityError:
                pass
            insert_to_table("Owned_by", f"{raw['id']},{get_trainer_id(trainer)}","pokemon_id,trainer_id")

if __name__ == '__main__':
    insert()
