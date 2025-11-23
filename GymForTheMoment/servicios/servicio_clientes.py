import sqlite3
import os
from modelos.cliente import Cliente

class ServicioClientes:

    def __init__(self, db_path="gimnasio.db"):
        self.db_path = db_path
        self._crear_tabla()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _crear_tabla(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE,
                email TEXT,
                contrasena TEXT,
                pagado INTEGER DEFAULT 0,
                rol TEXT
            )
        """)
        conn.commit()
        conn.close()

    def agregar_cliente(self, usuario, email, contrasena, pagado=False, rol="cliente"):
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO clientes (usuario, email, contrasena, pagado, rol)
                VALUES (?, ?, ?, ?, ?)
            """, (usuario, email, contrasena, int(bool(pagado)), rol))

            print(f"[DEBUG] INSERT → usuario={usuario}, pagado={int(bool(pagado))}")

            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return False
        conn.close()
        return True

    def obtener_cliente_por_usuario(self, usuario):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, usuario, email, contrasena, pagado, rol
            FROM clientes WHERE usuario=?
        """, (usuario,))
        fila = cursor.fetchone()
        conn.close()

        if fila:
            return Cliente(
                id=fila[0],
                usuario=fila[1],
                email=fila[2],
                contrasena=fila[3],
                pagado=bool(fila[4]),
                rol=fila[5]
            )
        return None

    def listar_clientes(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, usuario, email, contrasena, pagado, rol FROM clientes
        """)
        filas = cursor.fetchall()
        conn.close()

        return [
            Cliente(
                id=f[0],
                usuario=f[1],
                email=f[2],
                contrasena=f[3],
                pagado=bool(f[4]),
                rol=f[5]
            )
            for f in filas
        ]

    def listar_clientes_bd(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT usuario, email, pagado, rol FROM clientes
        """)
        filas = cursor.fetchall()
        conn.close()

        return [
            {
                "usuario": fila[0],
                "email": fila[1],
                "pagado": int(fila[2]),
                "rol": fila[3]
            }
            for fila in filas
        ]

    def actualizar_estado_pago(self, usuario, pagado):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes SET pagado=? WHERE usuario=?
        """, (int(bool(pagado)), usuario))

        print(f"[DEBUG] UPDATE → usuario={usuario}, pagado={int(bool(pagado))}")

        conn.commit()
        conn.close()

    def marcar_pagado(self, usuario):
        self.actualizar_estado_pago(usuario, True)

    def crear_usuarios_iniciales(self):
        if not self.obtener_cliente_por_usuario("Cliente1"):
            self.agregar_cliente("Cliente1", "cliente@gym.com", "cliente123")
            self.actualizar_estado_pago("Cliente1", True)

        if not self.obtener_cliente_por_usuario("Admin"):
            self.agregar_cliente("Admin", "admin@gym.com", "admin123", rol="administrador")
            self.actualizar_estado_pago("Admin", True)
