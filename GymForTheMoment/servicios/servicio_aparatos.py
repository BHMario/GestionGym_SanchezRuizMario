import sqlite3
import threading
import time
import datetime
from modelos.aparato import Aparato

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
                musculo TEXT,
                ocupante TEXT,
                hora_fin_ocupacion TEXT
            )
        """)
        conn.commit()

        # Migración: agregar columnas si no existen
        cursor.execute("PRAGMA table_info(aparatos)")
        columnas = [col[1] for col in cursor.fetchall()]
        if "ocupante" not in columnas:
            cursor.execute("ALTER TABLE aparatos ADD COLUMN ocupante TEXT")
        if "hora_fin_ocupacion" not in columnas:
            cursor.execute("ALTER TABLE aparatos ADD COLUMN hora_fin_ocupacion TEXT")
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

    def obtener_aparato_por_nombre(self, nombre):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, ocupado, musculo FROM aparatos WHERE nombre=?", (nombre,))
        fila = cursor.fetchone()
        conn.close()
        if fila:
            return Aparato(fila[0], fila[1], bool(fila[3]), fila[2], fila[4])
        return None

    def marcar_ocupado_por_nombre(self, nombre, minutos=30, cliente=""):
        # Marcar el aparato como ocupado y lanzar un hilo que lo libera tras 30 minutos.
        def ocupacion_temporal():
            hora_inicio = datetime.datetime.now()
            hora_fin = hora_inicio + datetime.timedelta(minutes=minutos)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE aparatos SET ocupado=1, ocupante=?, hora_fin_ocupacion=? WHERE nombre=?",
                          (cliente, hora_fin.strftime("%Y-%m-%d %H:%M:%S"), nombre))
            conn.commit()
            conn.close()

            time.sleep(minutos * 60)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE aparatos SET ocupado=0, ocupante=NULL, hora_fin_ocupacion=NULL WHERE nombre=?", (nombre,))
            conn.commit()
            conn.close()

        threading.Thread(target=ocupacion_temporal, daemon=True).start()

    def listar_aparatos_ocupados(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, ocupado, musculo, ocupante, hora_fin_ocupacion FROM aparatos WHERE ocupado=1")
        filas = cursor.fetchall()
        conn.close()
        resultados = []
        for f in filas:
            ocupante = f[5] if f[5] is not None else "N/A"
            hora_fin = f[6] if f[6] is not None else None
            resultados.append({"id": f[0], "nombre": f[1], "ocupante": ocupante, "hora_fin": hora_fin})
        return resultados

    def obtener_aparatos_por_cliente(self, cliente):
        """Retorna todos los aparatos actualmente ocupados por un cliente específico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, descripcion, ocupado, musculo, ocupante, hora_fin_ocupacion 
            FROM aparatos 
            WHERE ocupado=1 AND ocupante=?
        """, (cliente,))
        filas = cursor.fetchall()
        conn.close()
        
        resultados = []
        for f in filas:
            hora_fin = f[6] if f[6] is not None else None
            resultados.append({
                "id": f[0], 
                "nombre": f[1], 
                "ocupante": f[5],
                "hora_fin": hora_fin
            })
        return resultados

    def obtener_resumen_ocupacion(self):
        """Retorna un resumen de ocupación: aparatos totales, ocupados, libres"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM aparatos")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM aparatos WHERE ocupado=1")
        ocupados = cursor.fetchone()[0]
        
        libres = total - ocupados
        
        conn.close()
        
        return {
            'total': total,
            'ocupados': ocupados,
            'libres': libres,
            'porcentaje_ocupacion': round((ocupados / total * 100), 2) if total > 0 else 0
        }

