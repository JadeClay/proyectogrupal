import mysql.connector
from mysql.connector import Error

# 
# DATOS DE CONEXION
#
CONFIG = {
    "host": "localhost",        # ip de la bd
    "port": 3306,               
    "user": "root",             
    "password": "",             
    "database": "sistema_grupal",  # nombre de la bd
    "charset": "utf8mb4"
}


def conectar():
    """
    Esta funcion abre una conexion a la base de datos y la devuelve.
    
    COMO SE USA (para acordarme despues):
    
        from conexion_bd import conectar
        
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios")
            resultados = cursor.fetchall()
            conexion.close()
    
    NO OLVIDARSE de cerrar la conexion cuando se termina de usar,
    sino se llena de conexiones abiertas y MySQL se pone nervioso.
    """
    try:
        # intentamos conectar con los datos de CONFIG
        conexion = mysql.connector.connect(**CONFIG)
        
        # si llegamos hasta aca, todo bien
        print("Conexion a MySQL exitosa!")
        return conexion
        
    except Error as e:
        # si algo salio mal, mostramos el error
        # (esto ayuda a saber que paso cuando no funciona)
        print(f"Error al conectar a MySQL: {e}")
        return None

# Verificar que la conexion esta bien
def probar_conexion():
    conexion = conectar()
    if conexion:
        print("Conexion funcionando correctamente")
        conexion.close()
        return True
    else:
        print("No se pudo conectar a la base de datos")
        return False

