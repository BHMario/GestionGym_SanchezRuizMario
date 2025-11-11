import sqlite3
from modelos.reserva import Reserva

class ServicioReservas:
    def __init__(self, db_path="gimnasio.db"):
        self.db_path = db_path
        self._crear_tabla()

    def _crear_tabla(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                aparato TEXT,
                hora TEXT,
                estado TEXT
            )
        """)
        conn.commit()
        conn.close()

    def listar_sesiones(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, cliente, aparato, hora, estado FROM reservas")
        filas = cursor.fetchall()
        conn.close()
        return [Reserva(*f) for f in filas]

    def listar_reservas_pendientes(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, cliente, aparato, hora, estado FROM reservas WHERE estado='pendiente'")
        filas = cursor.fetchall()
        conn.close()
        return [Reserva(*f) for f in filas]

    def listar_solicitudes_pendientes(self):
        return self.listar_reservas_pendientes()

    def aceptar_reserva(self, reserva):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE reservas SET estado='aceptada' WHERE id=?", (reserva.id,))
        conn.commit()
        conn.close()

    def denegar_reserva(self, reserva):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE reservas SET estado='denegada' WHERE id=?", (reserva.id,))
        conn.commit()
        conn.close()
