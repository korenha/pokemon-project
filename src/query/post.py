from pymysql import IntegrityError
import json
from connect import connection
from query import get,post
def add_pokemon(pok):
    insert_to_table("Pokemon", f"{pok['id']},'{pok['name']}',{pok['height']},{pok['weight']}", "id,name,height,weight")



def insert_to_table(table,values,fields=""):
    try:
        with connection.cursor() as cursor:
            query = f"INSERT into {table} ({fields}) values({values})"
            cursor.execute(query)
            connection.commit()
            print (f"succeed insert {values} into {table}")
    except IntegrityError:
        print ("existed")

def add_to_of_type(pok_id,types):
    for type in types:
        id= get.get_type_id(type)
        insert_to_table("Of_type", f"{pok_id},{get.get_type_id(type)}", "pokemon_id,type_id")