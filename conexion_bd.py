# ============================================================
# conexion_bd.py
# ============================================================
# Conexión a la base de datos MySQL y funciones de acceso a datos.
# Cambiá los datos de CONFIG según tu configuración.
# ============================================================

import mysql.connector
from mysql.connector import Error


# Datos de conexión (cambialos si es necesario)
CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "sistema_grupal",
    "charset": "utf8mb4"
}


# ============================================================
# CONEXIÓN
# ============================================================

def conectar():
    """
    Abre una conexión a MySQL y la devuelve.
    Devuelve None si no se pudo conectar.
    """
    try:
        conexion = mysql.connector.connect(**CONFIG)
        return conexion

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None


# ============================================================
# FUNCIONES CRUD - USUARIOS
# ============================================================

def buscar_usuario(email, password):
    """
    Busca un usuario por email y contraseña (activo = 1).
    Retorna una tupla (id, nombre, email) o None.
    """
    conexion = conectar()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        sql = """
            SELECT id, nombre, email
            FROM usuarios
            WHERE email = %s AND password = %s AND activo = 1
        """
        cursor.execute(sql, (email, password))
        return cursor.fetchone()

    except Error as e:
        print(f"Error al buscar usuario: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def buscar_usuario_por_id(id_usuario):
    """
    Busca un usuario por ID.
    Retorna una tupla (id, nombre, email, activo) o None.
    """
    conexion = conectar()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        sql = """
            SELECT id, nombre, email, activo
            FROM usuarios
            WHERE id = %s
        """
        cursor.execute(sql, (id_usuario,))
        return cursor.fetchone()

    except Error as e:
        print(f"Error al buscar usuario por ID: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def insertar_usuario(nombre, email, password, activo=1):
    """
    Inserta un nuevo usuario.
    Retorna el ID insertado o None si hubo error.
    """
    conexion = conectar()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        sql = """
            INSERT INTO usuarios (nombre, email, password, activo)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, email, password, activo))
        conexion.commit()
        return cursor.lastrowid

    except Error as e:
        print(f"Error al insertar usuario: {e}")
        conexion.rollback()
        return None

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def actualizar_usuario(id_usuario, nombre=None, email=None, password=None):
    """
    Actualiza los campos de un usuario (solo los no None).
    Retorna True si se actualizó, False si hubo error.
    """
    conexion = conectar()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        campos = []
        valores = []

        if nombre is not None:
            campos.append("nombre = %s")
            valores.append(nombre)
        if email is not None:
            campos.append("email = %s")
            valores.append(email)
        if password is not None:
            campos.append("password = %s")
            valores.append(password)

        if not campos:
            return False

        valores.append(id_usuario)
        sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, valores)
        conexion.commit()
        return cursor.rowcount > 0

    except Error as e:
        print(f"Error al actualizar usuario: {e}")
        conexion.rollback()
        return False

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def eliminar_usuario(id_usuario):
    """
    Elimina (desactiva) un usuario poniendo activo = 0.
    Retorna True si se eliminó, False si hubo error.
    """
    conexion = conectar()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        sql = "UPDATE usuarios SET activo = 0 WHERE id = %s"
        cursor.execute(sql, (id_usuario,))
        conexion.commit()
        return cursor.rowcount > 0

    except Error as e:
        print(f"Error al eliminar usuario: {e}")
        conexion.rollback()
        return False

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()

# ============================================================
# FUNCIONES CRUD - CLIENTES
# ============================================================

# Funcion para insertar un cliente nuevo en la BD.
# Retorna (id, None) si salio bien, o (None, "mensaje_error") si falló.
# Si el email ya existe, MySQL lanza un error UNIQUE y se retorna ese mensaje.
def insertar_cliente(nombre, email, telefono):
    conexion = conectar()
    if not conexion:
        return None, "No se pudo conectar a la base de datos"

    try:
        cursor = conexion.cursor()
        sql = """
            INSERT INTO clientes (nombre, email, telefono, activo)
            VALUES (%s, %s, %s, 1)
        """
        cursor.execute(sql, (nombre, email, telefono))
        conexion.commit()
        return cursor.lastrowid, None

    except Error as e:
        # Si falla (ej: email duplicado, campo vacio), devolvemos el mensaje de MySQL
        conexion.rollback()
        return None, str(e)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def buscar_clientes(texto=""):
    """
    Busca clientes por nombre, email o telefono (activo = 1).
    Si texto está vacío, retorna todos los clientes activos.
    Retorna una lista de tuplas (id, nombre, email, telefono).
    """
    conexion = conectar()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        if texto:
            sql = """
                SELECT id, nombre, email, telefono
                FROM clientes
                WHERE activo = 1 AND (
                    nombre LIKE %s OR email LIKE %s OR telefono LIKE %s
                )
                ORDER BY nombre
            """
            patron = f"%{texto}%"
            cursor.execute(sql, (patron, patron, patron))
        else:
            sql = """
                SELECT id, nombre, email, telefono
                FROM clientes
                WHERE activo = 1
                ORDER BY nombre
            """
            cursor.execute(sql)
        return cursor.fetchall()

    except Error as e:
        print(f"Error al buscar clientes: {e}")
        return []

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def buscar_cliente_por_id(id_cliente):
    """
    Busca un cliente por ID (activo = 1).
    Retorna una tupla (id, nombre, email, telefono) o None.
    """
    conexion = conectar()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        sql = """
            SELECT id, nombre, email, telefono
            FROM clientes
            WHERE id = %s AND activo = 1
        """
        cursor.execute(sql, (id_cliente,))
        return cursor.fetchone()

    except Error as e:
        print(f"Error al buscar cliente por ID: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


# Funcion para actualizar los datos de un cliente.
# Solo actualiza los campos que no sean None.
# Retorna (True, None) si salio bien, o (False, "mensaje_error") si falló.
def actualizar_cliente(id_cliente, nombre=None, email=None, telefono=None):
    conexion = conectar()
    if not conexion:
        return False, "No se pudo conectar a la base de datos"

    try:
        cursor = conexion.cursor()
        campos = []
        valores = []

        if nombre is not None:
            campos.append("nombre = %s")
            valores.append(nombre)
        if email is not None:
            campos.append("email = %s")
            valores.append(email)
        if telefono is not None:
            campos.append("telefono = %s")
            valores.append(telefono)

        if not campos:
            return False, "No hay campos para actualizar"

        valores.append(id_cliente)
        sql = f"UPDATE clientes SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, valores)
        conexion.commit()
        return cursor.rowcount > 0, None

    except Error as e:
        # Si falla (ej: email duplicado), devolvemos el mensaje de MySQL
        conexion.rollback()
        return False, str(e)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


# Funcion para eliminar (desactivar) un cliente poniendo activo = 0.
# Retorna (True, None) si salio bien, o (False, "mensaje_error") si falló.
def eliminar_cliente(id_cliente):
    conexion = conectar()
    if not conexion:
        return False, "No se pudo conectar a la base de datos"

    try:
        cursor = conexion.cursor()
        sql = "UPDATE clientes SET activo = 0 WHERE id = %s"
        cursor.execute(sql, (id_cliente,))
        conexion.commit()
        return cursor.rowcount > 0, None

    except Error as e:
        # Si falla, devolvemos el mensaje de MySQL
        conexion.rollback()
        return False, str(e)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


# ============================================================
# FUNCIONES CRUD - VEHICULOS
# ============================================================

# Funcion para insertar un vehiculo nuevo en la BD.
# Retorna (id, None) si salio bien, o (None, "mensaje_error") si falló.
# Si la placa ya existe, MySQL lanza un error UNIQUE y se retorna ese mensaje.
def insertar_vehiculo(placa, marca, modelo, anio, cliente_id):
    conexion = conectar()
    if not conexion:
        return None, "No se pudo conectar a la base de datos"

    try:
        cursor = conexion.cursor()
        sql = """
            INSERT INTO vehiculos (placa, marca, modelo, anio, id_cliente, activo)
            VALUES (%s, %s, %s, %s, %s, 1)
        """
        cursor.execute(sql, (placa, marca, modelo, anio, cliente_id))
        conexion.commit()
        return cursor.lastrowid, None

    except Error as e:
        # Si falla (ej: placa duplicada, cliente inexistente), devolvemos el mensaje de MySQL
        conexion.rollback()
        return None, str(e)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def buscar_vehiculos(texto=""):
    """
    Busca vehiculos por placa, marca, modelo, anio (activo = 1).
    Si texto está vacío, retorna todos los vehiculos activos.
    Retorna una lista de tuplas (id, placa, marca, modelo, anio).
    """
    conexion = conectar()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        if texto:
            sql = """
                SELECT id, placa, marca, modelo, anio, id_cliente
                FROM vehiculos
                WHERE activo = 1 AND (
                    placa LIKE %s OR marca LIKE %s OR modelo LIKE %s OR anio LIKE %s
                )
                ORDER BY placa
            """
            patron = f"%{texto}%"
            cursor.execute(sql, (patron, patron, patron, patron))
        else:
            sql = """
                SELECT id, placa, marca, modelo, anio, id_cliente
                FROM vehiculos
                WHERE activo = 1
                ORDER BY placa
            """
            cursor.execute(sql)
        return cursor.fetchall()

    except Error as e:
        print(f"Error al buscar vehiculos: {e}")
        return []

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def buscar_vehiculo_por_id(id_vehiculo):
    """
    Busca un vehiculo por ID (activo = 1).
    Retorna una tupla (id, placa, marca, modelo, anio, id_cliente) o None.
    """
    conexion = conectar()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        sql = """
            SELECT id, placa, marca, modelo, anio, id_cliente
            FROM vehiculos
            WHERE id = %s AND activo = 1
        """
        cursor.execute(sql, (id_vehiculo,))
        return cursor.fetchone()

    except Error as e:
        print(f"Error al buscar cliente por ID: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


# Funcion para actualizar los datos de un vehiculo.
# Solo actualiza los campos que no sean None.
# Retorna (True, None) si salio bien, o (False, "mensaje_error") si falló.
def actualizar_vehiculo(id_vehiculo, placa=None, marca=None, modelo=None, anio=None, cliente_id=None):
    conexion = conectar()
    if not conexion:
        return False, "No se pudo conectar a la base de datos"

    try:
        cursor = conexion.cursor()
        campos = []
        valores = []

        if placa is not None:
            campos.append("placa = %s")
            valores.append(placa)
        if marca is not None:
            campos.append("marca = %s")
            valores.append(marca)
        if modelo is not None:
            campos.append("modelo = %s")
            valores.append(modelo)
        if anio is not None:
            campos.append("anio = %s")
            valores.append(anio)
        if cliente_id is not None:
            campos.append("id_cliente = %s")
            valores.append(cliente_id)

        if not campos:
            return False, "No hay campos para actualizar"

        valores.append(id_vehiculo)
        sql = f"UPDATE vehiculos SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, valores)
        conexion.commit()
        return cursor.rowcount > 0, None

    except Error as e:
        # Si falla (ej: placa duplicada), devolvemos el mensaje de MySQL
        conexion.rollback()
        return False, str(e)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


# Funcion para eliminar (desactivar) un vehiculo poniendo activo = 0.
# Retorna (True, None) si salio bien, o (False, "mensaje_error") si falló.
def eliminar_vehiculo(id_vehiculo):
    conexion = conectar()
    if not conexion:
        return False, "No se pudo conectar a la base de datos"

    try:
        cursor = conexion.cursor()
        sql = "UPDATE vehiculos SET activo = 0 WHERE id = %s"
        cursor.execute(sql, (id_vehiculo,))
        conexion.commit()
        return cursor.rowcount > 0, None

    except Error as e:
        # Si falla, devolvemos el mensaje de MySQL
        conexion.rollback()
        return False, str(e)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


# ============================================================
# FUNCIONES CRUD - SERVICIOS
# ============================================================

def insertar_servicio(id_vehiculo, fecha, costo, descripcion, estado="Pendiente"):
    """
    Inserta un nuevo servicio para un vehiculo.
    Retorna (id, None) si salio bien, o (None, "mensaje_error") si falló.
    """
    conexion = conectar()
    if not conexion:
        return None, "No se pudo conectar a la base de datos"

    try:
        cursor = conexion.cursor()
        sql = """
            INSERT INTO servicios (id_vehiculo, fecha, costo, descripcion, estado, activo)
            VALUES (%s, %s, %s, %s, %s, 1)
        """
        cursor.execute(sql, (id_vehiculo, fecha, costo, descripcion, estado))
        conexion.commit()
        return cursor.lastrowid, None

    except Error as e:
        conexion.rollback()
        return None, str(e)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def buscar_servicios(texto=""):
    """
    Busca servicios con informacion del vehiculo (activo = 1).
    Si texto esta vacio, retorna todos los servicios activos.
    Retorna una lista de tuplas (id, placa, fecha, costo, descripcion, estado, id_vehiculo).
    """
    conexion = conectar()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor()
        if texto:
            sql = """
                SELECT s.id, v.placa, s.fecha, s.costo, s.descripcion, s.estado, s.id_vehiculo
                FROM servicios s
                JOIN vehiculos v ON s.id_vehiculo = v.id
                WHERE s.activo = 1 AND (
                    v.placa LIKE %s OR s.descripcion LIKE %s
                )
                ORDER BY s.fecha DESC
            """
            patron = f"%{texto}%"
            cursor.execute(sql, (patron, patron))
        else:
            sql = """
                SELECT s.id, v.placa, s.fecha, s.costo, s.descripcion, s.estado, s.id_vehiculo
                FROM servicios s
                JOIN vehiculos v ON s.id_vehiculo = v.id
                WHERE s.activo = 1
                ORDER BY s.fecha DESC
            """
            cursor.execute(sql)
        return cursor.fetchall()

    except Error as e:
        print(f"Error al buscar servicios: {e}")
        return []

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def buscar_servicio_por_id(id_servicio):
    """
    Busca un servicio por ID (activo = 1).
    Retorna una tupla (id, id_vehiculo, fecha, costo, descripcion, estado) o None.
    """
    conexion = conectar()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()
        sql = """
            SELECT id, id_vehiculo, fecha, costo, descripcion, estado
            FROM servicios
            WHERE id = %s AND activo = 1
        """
        cursor.execute(sql, (id_servicio,))
        return cursor.fetchone()

    except Error as e:
        print(f"Error al buscar servicio por ID: {e}")
        return None

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def actualizar_servicio(id_servicio, fecha=None, costo=None, descripcion=None, estado=None):
    """
    Actualiza los campos de un servicio (solo los no None).
    Retorna (True, None) si salio bien, o (False, "mensaje_error") si falló.
    """
    conexion = conectar()
    if not conexion:
        return False, "No se pudo conectar a la base de datos"

    try:
        cursor = conexion.cursor()
        campos = []
        valores = []

        if fecha is not None:
            campos.append("fecha = %s")
            valores.append(fecha)
        if costo is not None:
            campos.append("costo = %s")
            valores.append(costo)
        if descripcion is not None:
            campos.append("descripcion = %s")
            valores.append(descripcion)
        if estado is not None:
            campos.append("estado = %s")
            valores.append(estado)

        if not campos:
            return False, "No hay campos para actualizar"

        valores.append(id_servicio)
        sql = f"UPDATE servicios SET {', '.join(campos)} WHERE id = %s"
        cursor.execute(sql, valores)
        conexion.commit()
        return cursor.rowcount > 0, None

    except Error as e:
        conexion.rollback()
        return False, str(e)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()


def eliminar_servicio(id_servicio):
    """
    Elimina (desactiva) un servicio poniendo activo = 0.
    Retorna (True, None) si salio bien, o (False, "mensaje_error") si falló.
    """
    conexion = conectar()
    if not conexion:
        return False, "No se pudo conectar a la base de datos"

    try:
        cursor = conexion.cursor()
        sql = "UPDATE servicios SET activo = 0 WHERE id = %s"
        cursor.execute(sql, (id_servicio,))
        conexion.commit()
        return cursor.rowcount > 0, None

    except Error as e:
        conexion.rollback()
        return False, str(e)

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conexion:
            conexion.close()

