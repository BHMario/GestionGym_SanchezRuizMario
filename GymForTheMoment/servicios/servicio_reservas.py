from servicios.base_datos import obtener_conexion
from modelos import Reserva

class ServicioReservas:
    def __init__(self):
        self.conexion = obtener_conexion()

    def agregar_reserva(self, reserva: Reserva):
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT INTO Reserva (aparato_id, cliente_id, fecha, hora_inicio, duracion_min, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (reserva.aparato_id, reserva.cliente_id, reserva.fecha, reserva.hora_inicio, reserva.duracion_min, reserva.estado))
        self.conexion.commit()
        reserva.reserva_id = cursor.lastrowid
        return reserva

    def listar_reservas_por_dia(self, fecha):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Reserva WHERE fecha=?", (fecha,))
        filas = cursor.fetchall()
        return [Reserva(*fila) for fila in filas]

    def listar_reservas_por_cliente(self, cliente_id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Reserva WHERE cliente_id=?", (cliente_id,))
        filas = cursor.fetchall()
        return [Reserva(*fila) for fila in filas]

    def obtener_reserva(self, reserva_id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Reserva WHERE reserva_id=?", (reserva_id,))
        fila = cursor.fetchone()
        if fila:
            return Reserva(*fila)
        return None

    def cancelar_reserva(self, reserva_id):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE Reserva SET estado='cancelado' WHERE reserva_id=?", (reserva_id,))
        self.conexion.commit()
