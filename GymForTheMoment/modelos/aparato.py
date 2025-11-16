class Aparato:
    def __init__(self, id, nombre, ocupado=False, descripcion="", musculo="General"):
        self.id = id
        self.nombre = nombre
        self.ocupado = ocupado
        self.descripcion = descripcion
        self.musculo = musculo

    def __repr__(self):
        return f"<Aparato {self.nombre} ({self.musculo}) - {'Ocupado' if self.ocupado else 'Libre'}>"
