"""
Script para crear automáticamente la base de datos Inventech en SQLite.
Ejecuta este script si aún no has creado la base de datos.
"""

import os
import sqlite3

DB_PATH = "inventech.db"


def leer_script_sql(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
        return None


def crear_base_datos():
    print("=" * 60)
    print("CREADOR DE BASE DE DATOS - INVENTECH (SQLite)")
    print("=" * 60)
    print(f"\nBase de datos: {DB_PATH}")

    try:
        if os.path.exists(DB_PATH):
            respuesta = input("\nBase de datos existente. ¿Sobrescribir? (s/n): ")
            if respuesta.lower() != "s":
                print("Operación cancelada")
                return False
            os.remove(DB_PATH)
            print("Base de datos anterior eliminada")

        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        ruta_script = os.path.join(os.path.dirname(__file__), "schema.sql")
        script_sql = leer_script_sql(ruta_script)
        if script_sql is None:
            return False

        cursor.executescript(script_sql)
        conexion.commit()

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table'")
        num_tablas = cursor.fetchone()[0]

        print(f"\nBase de datos creada exitosamente ({num_tablas} tablas)")

        for tabla in ("RolesUsuarios", "Usuarios", "Categorias", "Ubicaciones", "Proveedores"):
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            print(f"  - {tabla}: {cursor.fetchone()[0]} registros")

        cursor.close()
        conexion.close()

        print("\nEjecuta: python main.py")
        return True

    except sqlite3.Error as e:
        print(f"\nError en SQLite: {e}")
        return False


if __name__ == "__main__":
    if not crear_base_datos():
        print("\nAlternativa: elimina inventech.db y ejecuta schema.sql manualmente.")
