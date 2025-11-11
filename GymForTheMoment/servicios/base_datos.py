import sqlite3
import os

RUTA_BD = "datos/gimnasio.db"

def obtener_conexion():
    """
    Devuelve una conexión activa a la base de datos SQLite.
    Crea la carpeta 'datos/' si no existe.
    """
    if not os.path.exists("datos"):
        os.makedirs("datos")
    return sqlite3.connect(RUTA_BD)

def inicializar_bd():
    """
    Crea las tablas necesarias si no existen.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Crear tabla Cliente
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cliente (
        cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        email TEXT,
        telefono TEXT,
        fecha_alta DATE DEFAULT (date('now')),
        activo INTEGER DEFAULT 1
    );
    """)

    # Crear tabla Aparato
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Aparato (
        aparato_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        modelo TEXT,
        ubicacion TEXT,
        descripcion TEXT
    );
    """)

    # Crear tabla Reserva
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Reserva (
        reserva_id INTEGER PRIMARY KEY AUTOINCREMENT,
        aparato_id INTEGER NOT NULL,
        cliente_id INTEGER NOT NULL,
        fecha DATE NOT NULL,
        hora_inicio TEXT NOT NULL,
        duracion_min INTEGER NOT NULL DEFAULT 30,
        creado_en TIMESTAMP DEFAULT (datetime('now')),
        estado TEXT NOT NULL DEFAULT 'activo',
        FOREIGN KEY (aparato_id) REFERENCES Aparato(aparato_id) ON DELETE CASCADE,
        FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id) ON DELETE CASCADE
    );
    """)

    # Crear índice único para evitar reservas duplicadas exactas
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS ux_reserva_aparato_fecha_horaini
    ON Reserva(aparato_id, fecha, hora_inicio);
    """)

    # Crear tabla Recibo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Recibo (
        recibo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        año INTEGER NOT NULL,
        mes INTEGER NOT NULL,
        importe NUMERIC NOT NULL,
        generado_en TIMESTAMP DEFAULT (datetime('now')),
        pagado INTEGER DEFAULT 0,
        fecha_pago DATE,
        medio_pago TEXT,
        FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id) ON DELETE CASCADE,
        UNIQUE(cliente_id, año, mes)
    );
    """)

    conexion.commit()
    conexion.close()
