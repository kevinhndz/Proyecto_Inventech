import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="tu_usuario",
        password="tu_password",
        database="inventario"
    )
