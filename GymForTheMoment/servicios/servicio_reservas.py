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

    def crear_reserva(self, cliente, aparato, hora):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reservas (cliente, aparato, hora, estado) VALUES (?, ?, ?, ?)",
                       (cliente, aparato, hora, "pendiente"))
        conn.commit()
        conn.close()

    def aceptar_reserva(self, reserva):
        """
        Marca la reserva como aceptada y, si el 'aparato' corresponde a un aparato físico
        o a una clase, marca ese recurso como ocupado durante 30 minutos.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE reservas SET estado='aceptada' WHERE id=?", (reserva.id,))
        conn.commit()
        conn.close()

        # Intentar marcar el recurso como ocupado: primero intentamos con ServicioAparatos,
        # si no existe, intentamos con ServicioClases.
        try:
            # import aquí para evitar ciclos al importar interfaz <-> servicios
            from servicios.servicio_aparatos import ServicioAparatos
            s_aparatos = ServicioAparatos(self.db_path)
            aparato_obj = s_aparatos.obtener_aparato_por_nombre(reserva.aparato)
            if aparato_obj:
                s_aparatos.marcar_ocupado_por_nombre(reserva.aparato, minutos=30)
                return
        except Exception:
            # Si falla la importación o no encontrado, seguimos a clases
            pass

        try:
            from servicios.servicio_clases import ServicioClases
            s_clases = ServicioClases(self.db_path)
            clase_obj = s_clases.obtener_clase_por_nombre(reserva.aparato)
            if clase_obj:
                # ServicioClases ya implementa marcar_ocupado(nombre, minutos)
                s_clases.marcar_ocupado(reserva.aparato, minutos=30)
                return
        except Exception:
            pass

    def denegar_reserva(self, reserva):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE reservas SET estado='denegada' WHERE id=?", (reserva.id,))
        conn.commit()
        conn.close()
