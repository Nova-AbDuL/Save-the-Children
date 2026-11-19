"""
Prueba rápida del entorno. Cada integrante debe ejecutarla y compartir el resultado en el grupo:

    python src/prueba_entorno.py        (en Linux: python3 src/prueba_entorno.py)

Muestra las versiones de Python, Tkinter, ttkbootstrap y mysql-connector, y prueba la conexión.
"""

import platform
import sys

print("=== PRUEBA DE ENTORNO ===")
print("Python:", sys.version.split()[0], "-", platform.system())

try:
    import tkinter

    raiz = tkinter.Tk()
    raiz.update()
    raiz.destroy()
    print("Tkinter: OK (versión de Tk:", tkinter.TkVersion, ")")
except Exception as error:
    print("Tkinter: ERROR ->", error)
    print("  En Linux Mint instale: sudo apt install python3-tk")

try:
    import ttkbootstrap

    print("ttkbootstrap: OK (versión:", getattr(ttkbootstrap, "__version__", "desconocida"), ")")
except Exception as error:
    print("ttkbootstrap: ERROR ->", error)

try:
    import mysql.connector

    print("mysql-connector: OK (versión:", mysql.connector.__version__, ")")
except Exception as error:
    print("mysql-connector: ERROR ->", error)

try:
    from db.conexion import probar_conexion

    ok, detalle = probar_conexion()
    if ok:
        print("Conexión a MySQL: OK (versión del servidor:", detalle, ")")
    else:
        print("Conexión a MySQL: ERROR ->", detalle)
except (Exception, SystemExit) as error:
    print("Conexión a MySQL: no se pudo probar ->", error)
