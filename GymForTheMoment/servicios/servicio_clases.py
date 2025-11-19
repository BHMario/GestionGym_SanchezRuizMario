import sqlite3
from modelos.clase import Clase
import threading
import time

class ServicioClases:
    def __init__(self, db_path="gimnasio.db"):
        self.db_path = db_path
        self._crear_tabla()
        self._cargar_clases_iniciales()

    def _crear_tabla(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                descripcion TEXT,
                ocupado INTEGER,
                tipo TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _cargar_clases_iniciales(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clases")
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            clases_iniciales = [
                ("Yoga", "Clase de yoga para relajación y estiramiento.", 0, "Relax"),
                ("Pilates", "Clase de pilates para fuerza y postura.", 0, "Fuerza"),
                ("Spinning", "Clase de cardio intenso en bicicleta.", 0, "Cardio"),
                ("Zumba", "Clase de baile fitness.", 0, "Cardio"),
                ("Crossfit", "Entrenamiento funcional de alta intensidad.", 0, "Fuerza")
            ]
            cursor.executemany("""
                INSERT INTO clases (nombre, descripcion, ocupado, tipo)
                VALUES (?, ?, ?, ?)
            """, clases_iniciales)
            conn.commit()
        conn.close()

    def listar_clases(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, ocupado, tipo FROM clases")
        filas = cursor.fetchall()
        conn.close()
        return [Clase(f[0], f[1], bool(f[3]), f[2], f[4]) for f in filas]

    def obtener_clase_por_nombre(self, nombre):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, ocupado, tipo FROM clases WHERE nombre=?", (nombre,))
        fila = cursor.fetchone()
        conn.close()
        if fila:
            return Clase(fila[0], fila[1], bool(fila[3]), fila[2], fila[4])
        return None

    def marcar_ocupado(self, nombre_clase, minutos=30):
        # Marcar la clase como ocupada y lanzar un hilo que la libera tras 30 minutos.
        def ocupacion_temporal():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE clases SET ocupado=1 WHERE nombre=?", (nombre_clase,))
            conn.commit()
            conn.close()

            time.sleep(minutos * 60)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE clases SET ocupado=0 WHERE nombre=?", (nombre_clase,))
            conn.commit()
            conn.close()

        threading.Thread(target=ocupacion_temporal, daemon=True).start()
