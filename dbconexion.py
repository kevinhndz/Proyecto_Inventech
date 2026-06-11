import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def agrega_materials():
    """Add materials to database."""
    pass

def borra_materials():
    pass


if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Conexion exitosa a MySQL")
        conn.close()
    except Exception as e:
        print(" Error en la conexionn:", e)
