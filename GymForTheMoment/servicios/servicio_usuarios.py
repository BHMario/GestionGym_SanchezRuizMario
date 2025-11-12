import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "gimnasio.db"

class ServicioUsuarios:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self._crear_tabla()
        self.crear_usuarios_iniciales()

    def _crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('cliente','administrador'))
        )
        """)
        self.conn.commit()

    def obtener_usuario_por_usuario(self, usuario):
        self.cursor.execute(
            "SELECT id, usuario, contrasena, rol FROM usuarios WHERE usuario = ?", (usuario,)
        )
        fila = self.cursor.fetchone()
        if fila:
            return {"id": fila[0], "usuario": fila[1], "contrasena": fila[2], "rol": fila[3]}
        return None

    def crear_usuario(self, usuario, contrasena, rol="cliente"):
        try:
            self.cursor.execute(
                "INSERT INTO usuarios (usuario, contrasena, rol) VALUES (?, ?, ?)",
                (usuario, contrasena, rol)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def crear_usuarios_iniciales(self):
        if not self.obtener_usuario_por_usuario("cliente"):
            self.crear_usuario("cliente", "cliente123", "cliente")
        if not self.obtener_usuario_por_usuario("admin"):
            self.crear_usuario("admin", "admin123", "administrador")
