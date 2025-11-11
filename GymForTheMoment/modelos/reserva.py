class Reserva:
    def __init__(self, reserva_id=None, aparato_id=None, cliente_id=None, fecha=None, hora_inicio="", duracion_min=30, estado="activo"):
        self.reserva_id = reserva_id
        self.aparato_id = aparato_id
        self.cliente_id = cliente_id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.duracion_min = duracion_min
        self.estado = estado

    def __str__(self):
        return f"[{self.reserva_id}] Aparato: {self.aparato_id}, Cliente: {self.cliente_id}, Fecha: {self.fecha}, Hora: {self.hora_inicio}, Estado: {self.estado}"

    def to_dict(self):
        return {
            "reserva_id": self.reserva_id,
            "aparato_id": self.aparato_id,
            "cliente_id": self.cliente_id,
            "fecha": self.fecha,
            "hora_inicio": self.hora_inicio,
            "duracion_min": self.duracion_min,
            "estado": self.estado
        }
