# Estos métodos deben agregarse al final de servicio_clases.py

    def obtener_clases_por_cliente(self, cliente):
        """Retorna todas las clases actualmente ocupadas por un cliente específico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, ocupado, tipo, ocupante, hora_fin_ocupacion FROM clases WHERE ocupado=1 AND ocupante=?", (cliente,))
        filas = cursor.fetchall()
        conn.close()
        resultados = []
        for f in filas:
            hora_fin = f[6] if f[6] is not None else None
            resultados.append({"id": f[0], "nombre": f[1], "ocupante": f[5], "hora_fin": hora_fin})
        return resultados

    def obtener_resumen_ocupacion(self):
        """Retorna un resumen de ocupación: clases totales, ocupadas, libres"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clases")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM clases WHERE ocupado=1")
        ocupadas = cursor.fetchone()[0]
        libres = total - ocupadas
        conn.close()
        return {
            'total': total, 
            'ocupadas': ocupadas, 
            'libres': libres, 
            'porcentaje_ocupacion': round((ocupadas / total * 100), 2) if total > 0 else 0
        }
