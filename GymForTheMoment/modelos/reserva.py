class Reserva:
    def __init__(self, id, cliente, aparato, hora_inicio, hora_fin, estado="pendiente"):
        self.id = id
        self.cliente = cliente
        self.aparato = aparato
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado

    def __repr__(self):
        return f"<Reserva {self.cliente} {self.aparato} {self.hora_inicio} - {self.hora_fin} - {self.estado}>"
