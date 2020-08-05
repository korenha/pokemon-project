import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1",
    db="pokemon_data",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)