class Aparato:
    def __init__(self, id, nombre, ocupado=False):
        self.id = id
        self.nombre = nombre
        self.ocupado = ocupado

    def __repr__(self):
        return f"<Aparato {self.nombre} - {'Ocupado' if self.ocupado else 'Libre'}>"
