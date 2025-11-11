class Recibo:
    def __init__(self, id, cliente, mes, pagado=False):
        self.id = id
        self.cliente = cliente
        self.mes = mes
        self.pagado = pagado

    def __repr__(self):
        return f"<Recibo {self.cliente} - {self.mes} - {'Pagado' if self.pagado else 'Moroso'}>"
