import sqlite3

def conectar():
    return sqlite3.connect("bot.db")

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telefono TEXT UNIQUE,
        nombre TEXT,
        estado TEXT DEFAULT 'inicio'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telefono TEXT,
        mensaje TEXT,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def guardar_usuario(numero):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO usuarios (telefono)
    VALUES (?)
    """, (numero,))

    conn.commit()
    conn.close()


def guardar_mensaje(numero, mensaje):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO mensajes (telefono, mensaje)
    VALUES (?, ?)
    """, (numero, mensaje))

    conn.commit()
    conn.close()


def obtener_estado(numero):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT estado FROM usuarios WHERE telefono = ?
    """, (numero,))

    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else "inicio"


def actualizar_estado(numero, estado):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios SET estado = ?
    WHERE telefono = ?
    """, (estado, numero))

    conn.commit()
    conn.close()


def guardar_nombre(numero, nombre):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios SET nombre = ?
    WHERE telefono = ?
    """, (nombre, numero))

    conn.commit()
    conn.close()   
    
def obtener_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT telefono, nombre FROM usuarios")
    datos = cursor.fetchall()

    conn.close()
    return datos


def obtener_mensajes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT telefono, mensaje, fecha FROM mensajes ORDER BY fecha DESC")
    datos = cursor.fetchall()

    conn.close()
    return datos
def verificar_admin(usuario, contrasena):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM admins WHERE usuario = ? AND contrasena = ?",
        (usuario, contrasena)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def crear_admin_inicial():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        contrasena TEXT
    )
    """)
    # Admin por defecto: admin / admin123 (cámbialo después)
    cursor.execute(
        "INSERT OR IGNORE INTO admins (usuario, contrasena) VALUES (?, ?)",
        ("admin", "admin123")
    )
    conn.commit()
    conn.close()