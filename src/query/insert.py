from src.connect import connection


def insert_to_table(name_table, values, fields=""):
    with connection.cursor() as cursor:
        query = f"INSERT into {name_table}{fields} values ({values});"
        cursor.execute(query)
        connection.commit()


def new_query(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = []
            item = cursor.fetchone()
            while item:
                result.append(item["name"])
                item = cursor.fetchone()
            return result

    except Exception as ex:
        return "Error"


