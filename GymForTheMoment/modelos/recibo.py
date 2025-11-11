class Recibo:
    def __init__(self, recibo_id=None, cliente_id=None, año=None, mes=None, importe=0.0, pagado=False, fecha_pago=None, medio_pago=None):
        self.recibo_id = recibo_id
        self.cliente_id = cliente_id
        self.año = año
        self.mes = mes
        self.importe = importe
        self.pagado = pagado
        self.fecha_pago = fecha_pago
        self.medio_pago = medio_pago

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"[{self.recibo_id}] Cliente: {self.cliente_id}, {self.mes}/{self.año}, Importe: {self.importe}, {estado}"

    def to_dict(self):
        return {
            "recibo_id": self.recibo_id,
            "cliente_id": self.cliente_id,
            "año": self.año,
            "mes": self.mes,
            "importe": self.importe,
            "pagado": self.pagado,
            "fecha_pago": self.fecha_pago,
            "medio_pago": self.medio_pago
        }
