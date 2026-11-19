import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="TU USUARIO",
    password="TU CONTRASEÑA",
    database="TUBASEDEDATOS",
)

print("Conectado:", conexion.is_connected())
conexion.close()