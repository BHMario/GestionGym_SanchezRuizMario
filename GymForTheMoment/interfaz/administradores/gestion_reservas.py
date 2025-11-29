import tkinter as tk
from tkinter import ttk
from servicios.servicio_reservas import ServicioReservas
from servicios.servicio_aparatos import ServicioAparatos
from servicios.servicio_clases import ServicioClases
import datetime

class VentanaGestionReservas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Reservas - Gym For The Moment")
        self.root.geometry("1000x700")
        self.root.configure(bg="#FFFFFF")

        self.servicio_reservas = ServicioReservas()
        self.servicio_aparatos = ServicioAparatos()
        self.servicio_clases = ServicioClases()

        self._configurar_estilos()
        self._construir_interfaz()

        # Actualizar periódicamente
        self._cargar_datos()
        self.root.after(3000, self._actualizar_periodicamente)

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#FFFFFF", foreground="#222222", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 11, "bold"))

    def _construir_interfaz(self):
        # Título
        tk.Label(self.root, text="Gestión de Reservas", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(pady=(25, 10))

        tk.Label(self.root, text="Máquinas y clases ocupadas actualmente", bg="#FFFFFF",
                 fg="#666666", font=("Segoe UI", 11)).pack(pady=(0, 15))

        # Canvas con scrollbar
        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window_id, width=e.width))
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_limited)

    def _on_mousewheel_limited(self, event):
        delta = int(-1 * (event.delta / 120) * 30)
        y1, y2 = self.canvas.yview()
        if (delta < 0 and y1 <= 0) or (delta > 0 and y2 >= 1):
            return
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _cargar_datos(self):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()

        aparatos_ocupados = self.servicio_aparatos.listar_aparatos_ocupados()
        clases_ocupadas = self.servicio_clases.listar_clases_ocupadas()

        if not aparatos_ocupados and not clases_ocupadas:
            tk.Label(self.scrollable_frame, text="No hay máquinas ni clases ocupadas en este momento",
                    bg="#FFFFFF", fg="#888888", font=("Segoe UI", 14)).pack(pady=40)
            return

        # Sección de aparatos
        if aparatos_ocupados:
            tk.Label(self.scrollable_frame, text="🏋️ Máquinas Ocupadas", bg="#FFFFFF", fg="#222222",
                    font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))

            for aparato in aparatos_ocupados:
                self._crear_tarjeta_ocupacion(aparato, "aparato")

        # Sección de clases
        if clases_ocupadas:
            tk.Label(self.scrollable_frame, text="📚 Clases Ocupadas", bg="#FFFFFF", fg="#222222",
                    font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=(20, 5))

            for clase in clases_ocupadas:
                self._crear_tarjeta_ocupacion(clase, "clase")

    def _crear_tarjeta_ocupacion(self, item, tipo):
        tarjeta_frame = tk.Frame(self.scrollable_frame, bg="#F0F7FF", relief="solid", bd=1)
        tarjeta_frame.pack(fill="x", pady=8, padx=5)

        contenido = tk.Frame(tarjeta_frame, bg="#F0F7FF")
        contenido.pack(fill="both", expand=True, padx=15, pady=12)

        # Primera fila: Nombre
        nombre_frame = tk.Frame(contenido, bg="#F0F7FF")
        nombre_frame.pack(fill="x", pady=(0, 8))

        icono = "🏋️" if tipo == "aparato" else "📚"
        tk.Label(nombre_frame, text=f"{icono} {item.get('nombre','N/A')}", bg="#F0F7FF", fg="#222222",
                font=("Segoe UI", 13, "bold"), wraplength=800, justify="left").pack(side="left")

        # Segunda fila: Ocupante y horario
        info_frame = tk.Frame(contenido, bg="#F0F7FF")
        info_frame.pack(fill="x", pady=(0, 5))

        tk.Label(info_frame, text=f"Ocupante: ", bg="#F0F7FF", fg="#666666",
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(info_frame, text=f"{item.get('ocupante','N/A')}", bg="#F0F7FF", fg="#2196F3",
                font=("Segoe UI", 10, "bold"), wraplength=300, justify="left").pack(side="left", padx=(0, 20))

        # Calcular tiempo restante
        try:
            hora_fin_text = item.get('hora_fin')
            if hora_fin_text in (None, '', 'None'):
                raise ValueError("hora_fin no disponible")
            hora_fin = datetime.datetime.strptime(hora_fin_text, "%Y-%m-%d %H:%M:%S")
            ahora = datetime.datetime.now()
            diferencia = hora_fin - ahora

            if diferencia.total_seconds() > 0:
                minutos = int(diferencia.total_seconds() // 60)
                segundos = int(diferencia.total_seconds() % 60)
                tiempo_restante = f"{minutos}m {segundos}s"
            else:
                tiempo_restante = "Finalizando..."
        except Exception:
            tiempo_restante = "N/A"

        tk.Label(info_frame, text=f"Tiempo restante: ", bg="#F0F7FF", fg="#666666",
                font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(info_frame, text=f"{tiempo_restante}", bg="#F0F7FF", fg="#FF9800",
                font=("Segoe UI", 10, "bold")).pack(side="left")

        # Tercera fila: Hora de fin
        hora_frame = tk.Frame(contenido, bg="#F0F7FF")
        hora_frame.pack(fill="x")

        tk.Label(hora_frame, text=f"Hora de fin: ", bg="#F0F7FF", fg="#666666",
                font=("Segoe UI", 10, "bold")).pack(side="left")
        hora_fin_display = item.get('hora_fin') if item.get('hora_fin') not in (None, '', 'None') else 'N/A'
        tk.Label(hora_frame, text=f"{hora_fin_display}", bg="#F0F7FF", fg="#222222",
                font=("Segoe UI", 10), wraplength=400, justify="left").pack(side="left")

        # Efecto hover
        def on_enter(e):
            tarjeta_frame.configure(bg="#E3F2FD")
            contenido.configure(bg="#E3F2FD")
            nombre_frame.configure(bg="#E3F2FD")
            info_frame.configure(bg="#E3F2FD")
            hora_frame.configure(bg="#E3F2FD")

        def on_leave(e):
            tarjeta_frame.configure(bg="#F0F7FF")
            contenido.configure(bg="#F0F7FF")
            nombre_frame.configure(bg="#F0F7FF")
            info_frame.configure(bg="#F0F7FF")
            hora_frame.configure(bg="#F0F7FF")

        tarjeta_frame.bind("<Enter>", on_enter)
        tarjeta_frame.bind("<Leave>", on_leave)

    def _actualizar_periodicamente(self):
        if self.root.winfo_exists():
            self._cargar_datos()
            self.root.after(3000, self._actualizar_periodicamente)
