"""
Conexión a MySQL y funciones básicas para ejecutar consultas.

Uso desde cualquier módulo (ejecutando el programa con: python src/main.py):

    from db.conexion import ejecutar_consulta, ejecutar_accion

    voluntarios = ejecutar_consulta("SELECT * FROM voluntario WHERE id_estado_vol = %s", (2,))
    nuevo_id = ejecutar_accion("INSERT INTO donante (nombres) VALUES (%s)", ("Marta Quispe",))

IMPORTANTE: siempre use parámetros (%s) y no arme las consultas con f-strings,
para evitar errores y problemas de seguridad (inyección SQL).
"""

import mysql.connector
from mysql.connector import Error

try:
    from config import DB_CONFIG
except ImportError:
    raise SystemExit(
        "Falta el archivo src/config.py.\n"
        "Copie src/config_ejemplo.py como src/config.py y complete sus datos de MySQL."
    )


def obtener_conexion():
    """Abre y devuelve una conexión nueva a la base de datos."""
    return mysql.connector.connect(**DB_CONFIG)


def probar_conexion():
    """Devuelve (True, versión) si se conecta, o (False, mensaje_de_error)."""
    try:
        conexion = obtener_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            cursor.close()
        finally:
            conexion.close()
        return True, version
    except Error as error:
        return False, str(error)


def ejecutar_consulta(sql, parametros=None):
    """
    Ejecuta un SELECT y devuelve una lista de diccionarios.
    Ejemplo de resultado: [{"id_voluntario": 1, "nombres": "Ana"}, ...]
    """
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, parametros or ())
        filas = cursor.fetchall()
        cursor.close()
        return filas
    finally:
        conexion.close()


def ejecutar_accion(sql, parametros=None):
    """
    Ejecuta un INSERT, UPDATE o DELETE y guarda los cambios (commit).
    Devuelve el id generado (en INSERT) o la cantidad de filas afectadas.
    Si ocurre un error, deshace el cambio (rollback) y vuelve a lanzar el error.
    """
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros or ())
        conexion.commit()
        resultado = cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        cursor.close()
        return resultado
    except Error:
        conexion.rollback()
        raise
    finally:
        conexion.close()
