import pymysql
import json
from initialization import connection

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
    query = f"SELECT P.name_ FROM Pokemon P JOIN Type T on P.type_id = T.id  WHERE T.name = '{type}';"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            ans = []
            result = cursor.fetchone()
            while result:
                ans.append(result["name_"])
                result = cursor.fetchone()
            return ans
    except Exception as ex:
        return {"Error": str(ex)}, 500

def find_owners(pok_name):
    query = f"SELECT T.name\
            FROM (SELECT O.trainer_id as id " \
                f"FROM Pokemon P JOIN OwnedBy O on P.id = O.pokemon_id " \
                f"WHERE P.name_ = '{pok_name}') J JOIN Trainer T on T.id = J.id"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            ans = []
            result = cursor.fetchone()
            while result:
                ans.append(result["name"])
                result = cursor.fetchone()
            return ans
    except Exception as ex:
        return {"Error": str(ex)}, 500


def find_roster(trainer_name):
    query = f"SELECT P.name_\
            FROM (SELECT O.pokemon_id as id " \
                f"FROM Trainer T JOIN OwnedBy O on T.id = O.trainer_id " \
                f"WHERE T.name = '{trainer_name}') J JOIN Pokemon P on P.id = J.id"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            ans = []
            result = cursor.fetchone()
            while result:
                ans.append(result["name_"])
                result = cursor.fetchone()
            return ans
    except Exception as ex:
        return {"Error": str(ex)}, 500
