from src.connect import connection
from .insert import insert_to_table
from pymysql import IntegrityError


def insert(num_pokemon, type_):
    try:
        num_trainer = get_type_id(type_)

        if num_trainer == -1:
            insert_to_table("types", f"'{type_}'", " (name)")
            num_trainer = get_type_id(type_)

        insert_to_table("of_type", f"{num_pokemon}, {num_trainer}")

    except IntegrityError as ex:
        print(f"DB Error - {ex}")


def add(num_pokemon, type_):
    if isinstance(type_, list):
        for item in type_:
            insert(num_pokemon, item)

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



