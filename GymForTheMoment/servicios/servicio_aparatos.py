import sqlite3
from modelos.aparato import Aparato

class ServicioAparatos:
    def __init__(self, db_path="gimnasio.db"):
        self.db_path = db_path
        self._crear_tabla()

    def _crear_tabla(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aparatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                ocupado INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def listar_aparatos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, ocupado FROM aparatos")
        filas = cursor.fetchall()
        conn.close()
        return [Aparato(f[0], f[1], bool(f[2])) for f in filas]
