from servicios.base_datos import obtener_conexion
from modelos import Aparato

class ServicioAparatos:
    def __init__(self):
        self.conexion = obtener_conexion()

    def agregar_aparato(self, aparato: Aparato):
        cursor = self.conexion.cursor()
        cursor.execute("""
            INSERT INTO Aparato (nombre, modelo, ubicacion, descripcion)
            VALUES (?, ?, ?, ?)
        """, (aparato.nombre, aparato.modelo, aparato.ubicacion, aparato.descripcion))
        self.conexion.commit()
        aparato.aparato_id = cursor.lastrowid
        return aparato

    def listar_aparatos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Aparato")
        filas = cursor.fetchall()
        return [Aparato(*fila) for fila in filas]

    def obtener_aparato(self, aparato_id):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM Aparato WHERE aparato_id=?", (aparato_id,))
        fila = cursor.fetchone()
        if fila:
            return Aparato(*fila)
        return None

    def actualizar_aparato(self, aparato: Aparato):
        cursor = self.c
