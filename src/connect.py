import pymysql

connection = pymysql.connect(
    host="localhost",
    user="DELL",
    password="",
    db="pokemon_data",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
