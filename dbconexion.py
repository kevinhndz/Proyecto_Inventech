import sqlite3
import os
from datetime import datetime

DB_PATH = "inventech.db"

def get_connection():
    """Establece conexión con la base de datos SQLite."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        conexion.row_factory = sqlite3.Row
        return conexion
    except sqlite3.Error as e:
        print(f"Error en la conexión: {e}")
        raise

def validar_cantidad(cantidad):
    """Valida que la cantidad sea un número positivo."""
    try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a 0"
        return True, cantidad
    except ValueError:
        return False, "La cantidad debe ser un número entero"

def validar_id(id_valor):
    """Valida que el ID sea un número positivo."""
    try:
        id_valor = int(id_valor)
        if id_valor <= 0:
            return False, "El ID debe ser mayor a 0"
        return True, id_valor
    except ValueError:
        return False, "El ID debe ser un número entero"

def validar_fecha(fecha_str):
    """Valida que la fecha esté en formato YYYY-MM-DD."""
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True, fecha_str
    except ValueError:
        return False, "La fecha debe estar en formato YYYY-MM-DD"

def validar_nombre(nombre):
    """Valida que el nombre no esté vacío."""
    if not nombre or len(nombre.strip()) == 0:
        return False, "El nombre no puede estar vacío"
    if len(nombre) > 100:
        return False, "El nombre es muy largo (máximo 100 caracteres)"
    return True, nombre.strip()

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Conexión exitosa a SQLite")
        conn.close()
    except Exception as e:
        print(f"✗ Error en la conexión: {e}")
