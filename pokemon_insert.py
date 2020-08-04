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
        query = f"SELECT id FROM Trainer WHERE name = '{trainer}'"
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
            insert_to_table("Owned_by", f"{raw['id']},{get_trainer_id(trainer['name'])}","pokemon_id,trainer_id")

if __name__ == '__main__':
    insert()
