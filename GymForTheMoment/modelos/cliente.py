class Cliente:
    def __init__(self, cliente_id=None, nombre="", apellidos="", email="", telefono="", fecha_alta=None, activo=True):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono
        self.fecha_alta = fecha_alta
        self.activo = activo

    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"[{self.cliente_id}] {self.nombre} {self.apellidos} - {estado}"

    def to_dict(self):
        return {
            "cliente_id": self.cliente_id,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "email": self.email,
            "telefono": self.telefono,
            "fecha_alta": self.fecha_alta,
            "activo": self.activo
        }
