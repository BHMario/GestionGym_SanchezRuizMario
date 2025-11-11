class Aparato:
    def __init__(self, aparato_id=None, nombre="", modelo="", ubicacion="", descripcion=""):
        self.aparato_id = aparato_id
        self.nombre = nombre
        self.modelo = modelo
        self.ubicacion = ubicacion
        self.descripcion = descripcion

    def __str__(self):
        return f"[{self.aparato_id}] {self.nombre} ({self.modelo}) - {self.ubicacion}"

    def to_dict(self):
        return {
            "aparato_id": self.aparato_id,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "ubicacion": self.ubicacion,
            "descripcion": self.descripcion
        }
