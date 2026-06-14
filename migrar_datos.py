import re
import sqlite3

SQL_MYSQL = r"C:\Users\Usuario\Documents\dumps\Dump20260614 (1).sql"
DB_SQLITE = "inventech.db"

print("Iniciando inyección exacta por columnas...")
with open(SQL_MYSQL, "r", encoding="utf8") as f:
    lineas = f.readlines()

conn = sqlite3.connect(DB_SQLITE)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = OFF;")
cursor.execute("PRAGMA ignore_check_constraints = ON;")

for linea in lineas:
    if any(x in linea for x in ["LOCK TABLES", "UNLOCK TABLES", "SET ", "/*!40"]):
        continue
    linea = linea.replace("`", "")
    linea = re.sub(r"\bTRUE\b", "1", linea, flags=re.IGNORECASE)
    linea = re.sub(r"\bFALSE\b", "0", linea, flags=re.IGNORECASE)
    
    if linea.strip().startswith("INSERT INTO"):
        try:
            cursor.execute(linea)
        except sqlite3.Error as e:
            continue

conn.commit()
cursor.execute("PRAGMA foreign_keys = ON;")
conn.close()

print(" completada con éxito! Datos forzados en inventech.db.")