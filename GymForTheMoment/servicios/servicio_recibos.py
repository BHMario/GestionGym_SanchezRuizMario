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

        for c in clientes:
            if c["pagado"]:
                cursor.execute("INSERT INTO recibos (cliente, mes, pagado) VALUES (?, ?, ?)",
                               (c["usuario"], mes, 1))
                recibos_generados.append(c)

        conn.commit()
        conn.close()

        if recibos_generados:
            archivo_nombre = f"recibos_{mes}.txt"
            with open(archivo_nombre, "w", encoding="utf-8") as f:
                f.write(f"Recibos de Clientes Pagados - {mes}\n")
                f.write("="*50 + "\n\n")
                for c in recibos_generados:
                    f.write(f"Usuario: {c['usuario']}\n")
                    f.write(f"Email: {c['email']}\n")
                    f.write("Estado de Pago: Pagado\n")
                    f.write("-"*50 + "\n")
            print(f"Archivo generado: {os.path.abspath(archivo_nombre)}")
        else:
            print("No hay clientes pagados para generar recibos.")

    def listar_morosos(self):
        clientes = self.servicio_clientes.listar_clientes_bd()
        return [c for c in clientes if not c["pagado"]]
