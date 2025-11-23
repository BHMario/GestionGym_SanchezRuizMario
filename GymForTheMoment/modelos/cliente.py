class Cliente:
    def __init__(self, id, usuario, email, contrasena, pagado=False, rol="cliente"):
        self.id = id
        self.usuario = usuario
        self.email = email
        self.contrasena = contrasena
        self.pagado = bool(pagado)
        self.rol = rol

    def __repr__(self):
        return f"<Cliente {self.usuario} ({self.rol}) - Pagado: {self.pagado}>"
