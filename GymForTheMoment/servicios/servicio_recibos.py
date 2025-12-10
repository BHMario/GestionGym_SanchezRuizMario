import sqlite3
from servicios.servicio_clientes import ServicioClientes
import datetime
import os

class ServicioRecibos:
    def __init__(self, db_path="gimnasio.db"):
        self.db_path = db_path
        self._crear_tabla()
        self.servicio_clientes = ServicioClientes(db_path)

    def _crear_tabla(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recibos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                mes TEXT,
                pagado INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def generar_recibos_mes(self, mes=None):
        if mes is None:
            mes = datetime.datetime.now().strftime("%Y-%m")
        clientes = self.servicio_clientes.listar_clientes_bd()
        recibos_generados = []

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # generar recibo para cada cliente si no existe ya uno para el mes
        for c in clientes:
            cursor.execute("SELECT COUNT(*) FROM recibos WHERE cliente=? AND mes=?", (c["usuario"], mes))
            if cursor.fetchone()[0] > 0:
                continue
            pagado_flag = 1 if c["pagado"] else 0
            cursor.execute("INSERT INTO recibos (cliente, mes, pagado) VALUES (?, ?, ?)",
                           (c["usuario"], mes, pagado_flag))
            recibos_generados.append({"usuario": c["usuario"], "email": c["email"], "pagado": pagado_flag})

        conn.commit()
        conn.close()

        if recibos_generados:
            archivo_nombre = f"recibos_{mes}.txt"
            with open(archivo_nombre, "w", encoding="utf-8") as f:
                f.write(f"Recibos de Clientes - {mes}\n")
                f.write("="*50 + "\n\n")
                for c in recibos_generados:
                    f.write(f"Usuario: {c['usuario']}\n")
                    f.write(f"Email: {c['email']}\n")
                    f.write(f"Estado de Pago: {'Pagado' if c['pagado'] else 'Moroso'}\n")
                    f.write("-"*50 + "\n")
            print(f"Archivo generado: {os.path.abspath(archivo_nombre)}")
        else:
            print("No se generaron nuevos recibos (ya existen para el mes)")

    def listar_morosos(self):
        # listar morosos según el mes actual a partir de la tabla recibos
        mes = datetime.datetime.now().strftime("%Y-%m")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT cliente FROM recibos WHERE mes=? AND pagado=0", (mes,))
        filas = cursor.fetchall()
        conn.close()
        return [f[0] for f in filas]

    def marcar_recibo_pagado(self, cliente, mes=None):
        """Marcar como pagado el recibo del cliente para el mes dado. Si no existe, lo crea marcado como pagado."""
        if mes is None:
            mes = datetime.datetime.now().strftime("%Y-%m")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM recibos WHERE cliente=? AND mes=?", (cliente, mes))
        fila = cursor.fetchone()
        if fila:
            cursor.execute("UPDATE recibos SET pagado=1 WHERE id=?", (fila[0],))
        else:
            cursor.execute("INSERT INTO recibos (cliente, mes, pagado) VALUES (?, ?, 1)", (cliente, mes))
        conn.commit()
        conn.close()
