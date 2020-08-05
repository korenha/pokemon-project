import pymysql
import json
from pokemon_insert import connection
import pokemon_insert
from pymysql import IntegrityError

def get_heaviest_pokemon():
    query = "SELECT * FROM Pokemon WHERE weight_ = (\
        SELECT MAX(weight_) FROM Pokemon\
        )"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            pokemon = cursor.fetchone()
            if not pokemon:
                return json.dumps({"Error": "pokemon does not exists"}), 404
            return json.dumps(pokemon)
    except Exception as ex:
        return {"Error": str(ex)}, 500


def find_by_type(type):
    type_id = pokemon_insert.get_type_id(type)
    query = f"SELECT Pokemon.name\
                FROM Pokemon JOIN Of_type on Pokemon.id = Of_type.pokemon_id\
                WHERE Of_type.type_id = {type_id} ;"
    try:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                ans = []
                result = cursor.fetchone()
                while result:
                    ans.append(result["name"])
                    result = cursor.fetchone()
                return ans,200
        except IntegrityError as ex:
            return "not found",404
    except Exception as ex:
        return {"Error": str(ex)}, 500

def find_owners(pok_name):
    query = f"SELECT T.name\
            FROM (SELECT O.trainer_id as id " \
                f"FROM Pokemon P JOIN Owned_By O on P.id = O.pokemon_id " \
                f"WHERE P.name = '{pok_name}') J JOIN Trainer T on T.id = J.id"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            ans = []
            result = cursor.fetchone()
            while result:
                ans.append(result["name"])
                result = cursor.fetchone()
            return ans,200
    except Exception as ex:
        return {"Error": str(ex)}, 500


def find_roster(trainer_name):
    query = f"SELECT P.name\
            FROM (SELECT O.pokemon_id as id " \
                f"FROM Trainer T JOIN Owned_By O on T.id = O.trainer_id " \
                f"WHERE T.name = '{trainer_name}') J JOIN Pokemon P on P.id = J.id"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            ans = []
            result = cursor.fetchone()
            while result:
                ans.append(result["name"])
                result = cursor.fetchone()
            return ans,200
    except Exception as ex:
        return {"Error": str(ex)}, 500
