import sqlite3
from modelos.aparato import Aparato
import threading
import time

class ServicioAparatos:
    def __init__(self, db_path="gimnasio.db"):
        self.db_path = db_path
        self._crear_tabla()
        self._cargar_aparatos_iniciales()

    def _crear_tabla(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aparatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                descripcion TEXT,
                ocupado INTEGER,
                musculo TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _cargar_aparatos_iniciales(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM aparatos")
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            aparatos_iniciales = [
                ("Extensión de cuádriceps #1", "Máquina para aislar cuádriceps con peso regulable.", 0, "Pierna"),
                ("Extensión de cuádriceps #2", "Segunda máquina de cuádriceps.", 0, "Pierna"),
                ("Curl femoral #1", "Máquina para isquiotibiales tumbado o sentado.", 0, "Pierna"),
                ("Curl femoral #2", "Segunda máquina de curl femoral.", 0, "Pierna"),
                ("Press banca", "Banco horizontal con barra para pecho.", 0, "Pecho"),
                ("Sentadilla guiada", "Máquina Smith para sentadillas.", 0, "Pierna"),
                ("Remo sentado", "Poleas para espalda media.", 0, "Espalda"),
                ("Press militar", "Máquina/Barra para hombros.", 0, "Hombros"),
                ("Elíptica", "Cardio de bajo impacto.", 0, "Cardio"),
                ("Bicicleta estática", "Bicicleta fija para cardio.", 0, "Cardio"),
                ("Cinta de correr", "Máquina para correr.", 0, "Cardio"),
                ("Dorsalera", "Jalón al pecho o tras nuca.", 0, "Espalda"),
                ("Pectoral contractor", "Máquina contractor para pecho.", 0, "Pecho"),
                ("Abductor", "Trabaja abductores de piernas.", 0, "Pierna"),
                ("Aductor", "Trabaja aductores de piernas.", 0, "Pierna")
            ]

            cursor.executemany("""
                INSERT INTO aparatos (nombre, descripcion, ocupado, musculo)
                VALUES (?, ?, ?, ?)
            """, aparatos_iniciales)
            conn.commit()
        conn.close()

    def listar_aparatos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, ocupado, musculo FROM aparatos")
        filas = cursor.fetchall()
        conn.close()
        return [Aparato(f[0], f[1], bool(f[3]), f[2], f[4]) for f in filas]

    def marcar_ocupado(self, nombre_aparato, minutos=30):
        """Marca un aparato como ocupado y lo libera automáticamente después de X minutos"""
        def ocupacion_temporal():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE aparatos SET ocupado=1 WHERE nombre=?", (nombre_aparato,))
            conn.commit()
            conn.close()

            # Esperar los minutos especificados
            time.sleep(minutos * 60)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE aparatos SET ocupado=0 WHERE nombre=?", (nombre_aparato,))
            conn.commit()
            conn.close()

        # Ejecutar en hilo separado para no bloquear la interfaz
        threading.Thread(target=ocupacion_temporal, daemon=True).start()
