import sqlite3
from modelos.cliente import Cliente

class ServicioClientes:
    def __init__(self, db_path="gimnasio.db"):
        self.db_path = db_path
        self._crear_tabla()

    def _crear_tabla(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE,
                email TEXT,
                contrasena TEXT,
                pagado INTEGER,
                rol TEXT
            )
        """)
        conn.commit()
        conn.close()

    def agregar_cliente(self, usuario, email, contrasena, pagado=False, rol="cliente"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO clientes (usuario, email, contrasena, pagado, rol)
                VALUES (?, ?, ?, ?, ?)
            """, (usuario, email, contrasena, int(pagado), rol))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return False  # Usuario ya existe
        conn.close()
        return True

    def obtener_cliente_por_usuario(self, usuario):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario, email, contrasena, pagado, rol FROM clientes WHERE usuario=?", (usuario,))
        fila = cursor.fetchone()
        conn.close()
        if fila:
            return Cliente(*fila)
        return None

    def listar_clientes(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario, email, contrasena, pagado, rol FROM clientes")
        filas = cursor.fetchall()
        conn.close()
        return [Cliente(*f) for f in filas]

    def crear_usuarios_iniciales(self):
        if not self.obtener_cliente_por_usuario("Cliente1"):
            self.agregar_cliente("Cliente1", "cliente@gym.com", "cliente123", pagado=True, rol="cliente")
        if not self.obtener_cliente_por_usuario("Admin"):
            self.agregar_cliente("Admin", "admin@gym.com", "admin123", pagado=True, rol="administrador")
