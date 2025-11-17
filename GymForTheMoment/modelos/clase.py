class Clase:
    def __init__(self, id, nombre, ocupado=False, descripcion="", tipo=""):
        self.id = id
        self.nombre = nombre
        self.ocupado = ocupado
        self.descripcion = descripcion
        self.tipo = tipo

    def __repr__(self):
        return f"<Clase {self.nombre} - {self.tipo} - {'Ocupada' if self.ocupado else 'Libre'}>"
