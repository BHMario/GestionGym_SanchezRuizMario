from servicios.base_datos import obtener_conexion
from modelos import Recibo

class ServicioRecibos:
    def __init__(self):
        self.conexion = obtener_conexion()

    def agregar_recibo(self, recibo: Recibo):
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT INTO Recibo (cliente_id, año, mes, importe, pagado, fecha_pago, medio_pago)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (recibo.cliente_id, recibo.año, recibo.mes, recibo.importe, int(recibo.pagado), recibo.fecha_pago, recibo.medio_pago))
        self.conexion.commit()
        recibo.recibo_id = cursor.lastrowid
        return recibo

    def listar_recibos_por_cliente(self, cliente_id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Recibo WHERE cliente_id=?", (cliente_id,))
        filas = cursor.fetchall()
        return [Recibo(*fila) for fila in filas]

    def listar_recibos_por_mes(self, año, mes):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Recibo WHERE año=? AND mes=?", (año, mes))
        filas = cursor.fetchall()
        return [Recibo(*fila) for fila in filas]

    def marcar_pagado(self, recibo_id, fecha_pago, medio_pago):
        cursor = self.conexion.cursor()
        cursor.execute("""
            UPDATE Recibo
            SET pagado=1, fecha_pago=?, medio_pago=?
            WHERE recibo_id=?
        """, (fecha_pago, medio_pago, recibo_id))
        self.conexion.commit()

    def obtener_recibo(self, recibo_id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Recibo WHERE recibo_id=?", (recibo_id,))
        fila = cursor.fetchone()
        if fila:
            return Recibo(*fila)
        return None
