import sqlite3
from modelos.reserva import Reserva

class ServicioReservas:
    def __init__(self, db_path="gimnasio.db"):
        self.db_path = db_path
        self._crear_tabla()

    def _crear_tabla(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                aparato TEXT,
                hora_inicio TEXT,
                hora_fin TEXT,
                estado TEXT
            )
        """)
        # migración: si la tabla existía con esquema antiguo, añadir columnas
        cursor.execute("PRAGMA table_info(reservas)")
        columnas = [c[1] for c in cursor.fetchall()]
        if "hora_inicio" not in columnas:
            try:
                cursor.execute("ALTER TABLE reservas ADD COLUMN hora_inicio TEXT")
            except Exception:
                pass
        if "hora_fin" not in columnas:
            try:
                cursor.execute("ALTER TABLE reservas ADD COLUMN hora_fin TEXT")
            except Exception:
                pass
        conn.commit()
        conn.close()

    def listar_sesiones(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, cliente, aparato, hora_inicio, hora_fin, estado FROM reservas")
        filas = cursor.fetchall()
        conn.close()
        return [Reserva(*f) for f in filas]

    def listar_reservas_pendientes(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, cliente, aparato, hora_inicio, hora_fin, estado FROM reservas WHERE estado='pendiente'")
        filas = cursor.fetchall()
        conn.close()
        return [Reserva(*f) for f in filas]

    def listar_solicitudes_pendientes(self):
        return self.listar_reservas_pendientes()

    def crear_reserva(self, cliente, aparato, hora):
        # hora: string ISO 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD HH:MM'
        import datetime
        try:
            if len(hora.split()) == 1:
                # fecha solo no válida
                raise ValueError
            hora_dt = datetime.datetime.strptime(hora, "%Y-%m-%d %H:%M:%S")
        except Exception:
            try:
                hora_dt = datetime.datetime.strptime(hora, "%Y-%m-%d %H:%M")
            except Exception:
                raise ValueError("Formato de hora inválido. Use 'YYYY-MM-DD HH:MM' o 'YYYY-MM-DD HH:MM:SS'")

        # Validar L-V (weekday 0..4)
        if hora_dt.weekday() > 4:
            raise ValueError("Solo se permiten reservas de Lunes a Viernes")

        hora_inicio = hora_dt
        hora_fin = hora_inicio + datetime.timedelta(minutes=30)

        # comprobar solapamientos para el mismo aparato (aceptadas o pendientes)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, cliente, aparato, hora_inicio, hora_fin, estado FROM reservas WHERE aparato = ?",
            (aparato,)
        )
        filas = cursor.fetchall()
        for f in filas:
            try:
                existente_inicio = datetime.datetime.strptime(f[3], "%Y-%m-%d %H:%M:%S")
                existente_fin = datetime.datetime.strptime(f[4], "%Y-%m-%d %H:%M:%S")
            except Exception:
                # intentar sin segundos
                try:
                    existente_inicio = datetime.datetime.strptime(f[3], "%Y-%m-%d %H:%M")
                    existente_fin = datetime.datetime.strptime(f[4], "%Y-%m-%d %H:%M")
                except Exception:
                    continue

            # overlap if inicio < existente_fin and fin > existente_inicio
            if hora_inicio < existente_fin and hora_fin > existente_inicio:
                conn.close()
                raise ValueError("El aparato ya tiene una reserva solapada en esa franja horaria")

        cursor.execute("INSERT INTO reservas (cliente, aparato, hora_inicio, hora_fin, estado) VALUES (?, ?, ?, ?, ?)",
                       (cliente, aparato, hora_inicio.strftime("%Y-%m-%d %H:%M:%S"), hora_fin.strftime("%Y-%m-%d %H:%M:%S"), "pendiente"))
        conn.commit()
        conn.close()

    def aceptar_reserva(self, reserva):
        # Marcar la reserva como aceptada y, si el 'aparato' corresponde a un aparato físico
        # o a una clase, marca ese recurso como ocupado durante 30 minutos.
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE reservas SET estado='aceptada' WHERE id=?", (reserva.id,))
        conn.commit()
        conn.close()

        try:
            # import aquí para evitar ciclos al importar interfaz <-> servicios
            from servicios.servicio_aparatos import ServicioAparatos
            s_aparatos = ServicioAparatos(self.db_path)
            aparato_obj = s_aparatos.obtener_aparato_por_nombre(reserva.aparato)
            if aparato_obj:
                s_aparatos.marcar_ocupado_por_nombre(reserva.aparato, minutos=30, cliente=reserva.cliente)
                return
        except Exception:
            pass

        try:
            from servicios.servicio_clases import ServicioClases
            s_clases = ServicioClases(self.db_path)
            clase_obj = s_clases.obtener_clase_por_nombre(reserva.aparato)
            if clase_obj:
                s_clases.marcar_ocupado(reserva.aparato, minutos=30, cliente=reserva.cliente)
                return
        except Exception:
            pass

    def denegar_reserva(self, reserva):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE reservas SET estado='denegada' WHERE id=?", (reserva.id,))
        conn.commit()
        conn.close()

    def listar_ocupacion_por_dia(self, aparato, fecha_str):
        """Devuelve lista de reservas del aparato para la fecha dada (YYYY-MM-DD)."""
        import datetime
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'")

        inicio_dia = datetime.datetime.combine(fecha, datetime.time(0, 0))
        fin_dia = datetime.datetime.combine(fecha, datetime.time(23, 59, 59))

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, cliente, aparato, hora_inicio, hora_fin, estado FROM reservas WHERE aparato = ? AND (hora_inicio BETWEEN ? AND ? OR hora_fin BETWEEN ? AND ?)",
            (aparato, inicio_dia.strftime("%Y-%m-%d %H:%M:%S"), fin_dia.strftime("%Y-%m-%d %H:%M:%S"), inicio_dia.strftime("%Y-%m-%d %H:%M:%S"), fin_dia.strftime("%Y-%m-%d %H:%M:%S"))
        )
        filas = cursor.fetchall()
        conn.close()
        return [Reserva(*f) for f in filas]

    def listar_ocupacion_por_dia_por_cliente(self, cliente, fecha_str):
        """Devuelve lista de reservas del cliente para la fecha dada (YYYY-MM-DD)."""
        import datetime
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'")

        inicio_dia = datetime.datetime.combine(fecha, datetime.time(0, 0))
        fin_dia = datetime.datetime.combine(fecha, datetime.time(23, 59, 59))

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, cliente, aparato, hora_inicio, hora_fin, estado FROM reservas WHERE cliente = ? AND (hora_inicio BETWEEN ? AND ? OR hora_fin BETWEEN ? AND ?)",
            (cliente, inicio_dia.strftime("%Y-%m-%d %H:%M:%S"), fin_dia.strftime("%Y-%m-%d %H:%M:%S"), inicio_dia.strftime("%Y-%m-%d %H:%M:%S"), fin_dia.strftime("%Y-%m-%d %H:%M:%S"))
        )
        filas = cursor.fetchall()
        conn.close()
        return [Reserva(*f) for f in filas]

    def generar_horario_ocupacion_por_dia(self, aparato, fecha_str):
        """
        Genera un listado exacto de horas ocupadas para un aparato en un día.
        Devuelve una lista de tuplas (hora_inicio, hora_fin, cliente) ordenadas.
        """
        import datetime
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'")

        reservas = self.listar_ocupacion_por_dia(aparato, fecha_str)
        horario_ocupado = []
        
        for reserva in reservas:
            try:
                inicio = datetime.datetime.strptime(reserva.hora_inicio, "%Y-%m-%d %H:%M:%S")
                fin = datetime.datetime.strptime(reserva.hora_fin, "%Y-%m-%d %H:%M:%S")
            except Exception:
                try:
                    inicio = datetime.datetime.strptime(reserva.hora_inicio, "%Y-%m-%d %H:%M")
                    fin = datetime.datetime.strptime(reserva.hora_fin, "%Y-%m-%d %H:%M")
                except Exception:
                    continue
            
            horario_ocupado.append({
                'inicio': inicio.strftime("%H:%M"),
                'fin': fin.strftime("%H:%M"),
                'cliente': reserva.cliente,
                'estado': reserva.estado
            })
        
        # Ordenar por hora de inicio
        horario_ocupado.sort(key=lambda x: x['inicio'])
        return horario_ocupado

    def generar_todas_horas_disponibles(self, aparato, fecha_str):
        """
        Genera un listado completo de todas las franjas horarias disponibles (30 min)
        para un aparato en un día, indicando cuáles están libres u ocupadas.
        """
        import datetime
        try:
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Formato de fecha inválido. Use 'YYYY-MM-DD'")

        # Generar todas las franjas posibles (00:00-23:30 en intervalos de 30 min)
        todas_franjas = []
        hora_actual = datetime.datetime.combine(fecha, datetime.time(0, 0))
        fin_dia = datetime.datetime.combine(fecha, datetime.time(23, 59, 59))
        
        while hora_actual < fin_dia:
            hora_siguiente = hora_actual + datetime.timedelta(minutes=30)
            todas_franjas.append({
                'inicio': hora_actual.strftime("%H:%M"),
                'fin': hora_siguiente.strftime("%H:%M"),
                'estado': 'libre',
                'cliente': None
            })
            hora_actual = hora_siguiente
        
        # Marcar como ocupadas las franjas que tienen reserva
        horario_ocupado = self.generar_horario_ocupacion_por_dia(aparato, fecha_str)
        
        for franja in todas_franjas:
            for ocupada in horario_ocupado:
                if franja['inicio'] == ocupada['inicio']:
                    franja['estado'] = 'ocupada'
                    franja['cliente'] = ocupada['cliente']
                    break
        
        return todas_franjas

