from servicios.base_datos import obtener_conexion
from modelos import Cliente

class ServicioClientes:
    def __init__(self):
        self.conexion = obtener_conexion()

    def agregar_cliente(self, cliente: Cliente):
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT INTO Cliente (nombre, apellidos, email, telefono, fecha_alta, activo)
            VALUES (?, ?, ?, ?, date('now'), ?)
        """, (cliente.nombre, cliente.apellidos, cliente.email, cliente.telefono, int(cliente.activo)))
        self.conexion.commit()
        cliente.cliente_id = cursor.lastrowid
        return cliente

    def listar_clientes(self, activos=True):
        cursor = self.conexion.cursor()
        if activos:
            cursor.execute("SELECT * FROM Cliente WHERE activo=1")
        else:
            cursor.execute("SELECT * FROM Cliente")
        filas = cursor.fetchall()
        return [Cliente(*fila) for fila in filas]

    def obtener_cliente(self, cliente_id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Cliente WHERE cliente_id=?", (cliente_id,))
        fila = cursor.fetchone()
        if fila:
            return Cliente(*fila)
        return None

    def marcar_inactivo(self, cliente_id):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE Cliente SET activo=0 WHERE cliente_id=?", (cliente_id,))
        self.conexion.commit()
