import sqlite3
from modelos.recibo import Recibo
from servicios.servicio_clientes import ServicioClientes

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

    def generar_recibos_mes(self, mes="2025-11"):
        clientes = self.servicio_clientes.listar_clientes()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for c in clientes:
            cursor.execute("INSERT INTO recibos (cliente, mes, pagado) VALUES (?, ?, ?)",
                           (c.usuario, mes, int(c.pagado)))
        conn.commit()
        conn.close()

    def listar_morosos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT cliente FROM recibos WHERE pagado=0")
        filas = cursor.fetchall()
        conn.close()
        morosos = []
        for f in filas:
            c = self.servicio_clientes.obtener_cliente_por_usuario(f[0])
            if c:
                morosos.append(c)
        return morosos
