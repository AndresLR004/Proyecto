import sqlite3
import os

path = os.path.dirname(os.path.realpath(__file__)) # path on ens trobem
sqlite3_database_path = os.path.join(path, "sqlite3_database.db") # path del fitxer de base de dades

# comprovo que no existeix el fitxer
assert (not os.path.isfile(sqlite3_database_path)), f"Ja existeix el fitxer {sqlite3_database_path}. Esborra'l si vols crear-lo de nou."

# https://www.pythonforbeginners.com/files/with-statement-in-python
with sqlite3.connect(sqlite3_database_path) as con:
    print("Base de dades oberta amb èxit");

    def execute_sql(sql):
        con.execute(sql)
        print(f"Executat: {sql}")

    execute_sql("CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL, unitats INTEGER NOT NULL)")
    execute_sql("INSERT INTO items (nom, unitats) VALUES ('ous', 6)")
    execute_sql("INSERT INTO items (nom, unitats) VALUES ('pomes', 10)")
    execute_sql("INSERT INTO items (nom, unitats) VALUES ('rentavaixelles', 1)")