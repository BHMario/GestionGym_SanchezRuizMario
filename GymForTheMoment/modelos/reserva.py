class Reserva:
    def __init__(self, id, cliente, aparato, hora, estado="pendiente"):
        self.id = id
        self.cliente = cliente
        self.aparato = aparato
        self.hora = hora
        self.estado = estado

    def __repr__(self):
        return f"<Reserva {self.cliente} {self.aparato} {self.hora} - {self.estado}>"
