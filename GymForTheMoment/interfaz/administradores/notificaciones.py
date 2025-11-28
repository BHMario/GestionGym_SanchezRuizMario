import tkinter as tk
from tkinter import ttk
from servicios.servicio_reservas import ServicioReservas
from servicios.servicio_clases import ServicioClases
from servicios.servicio_aparatos import ServicioAparatos

class VentanaNotificaciones:
    def __init__(self, root):
        self.root = root
        self.root.title("Notificaciones - Gym For The Moment")
        self.root.geometry("900x650")
        self.root.configure(bg="#FFFFFF")
        self.servicio_reservas = ServicioReservas()
        self.servicio_clases = ServicioClases()
        self.servicio_aparatos = ServicioAparatos()

        self._configurar_estilos()
        self._construir_interfaz()

        # Variable para almacenar la reserva seleccionada
        self.reserva_seleccionada = None

        # Actualizar la lista automáticamente
        self.cargar_notificaciones()
        self.root.after(5000, self.actualizar_periodicamente)

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#FFFFFF", foreground="#222222", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 11, "bold"))
        style.configure("Notificacion.TFrame", background="#F5F5F5", relief="ridge", borderwidth=1)

    def _construir_interfaz(self):
        # Título
        tk.Label(self.root, text="Notificaciones de Solicitudes de Clientes", bg="#FFFFFF",
                 fg="#222222", font=("Segoe UI", 22, "bold")).pack(pady=(25, 10))

        tk.Label(self.root, text="Gestiona las solicitudes pendientes de clientes", bg="#FFFFFF",
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

    def cargar_notificaciones(self):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()

        solicitudes = self.servicio_reservas.listar_solicitudes_pendientes()

        if not solicitudes:
            tk.Label(self.scrollable_frame, text="No hay solicitudes pendientes", bg="#FFFFFF",
                     fg="#888888", font=("Segoe UI", 14)).pack(pady=40)
            return

        for solicitud in solicitudes:
            self._crear_tarjeta_notificacion(solicitud)

    def actualizar_periodicamente(self):
        self.cargar_notificaciones()
        self.root.after(5000, self.actualizar_periodicamente)

    def _crear_tarjeta_notificacion(self, solicitud):
        tarjeta_frame = tk.Frame(self.scrollable_frame, bg="#F5F5F5", relief="solid", bd=1)
        tarjeta_frame.pack(fill="x", pady=10, padx=5)

        # Contenido principal
        contenido = tk.Frame(tarjeta_frame, bg="#F5F5F5")
        contenido.pack(fill="both", expand=True, padx=15, pady=12)

        # Primera fila: Cliente y Aparato
        titulo_frame = tk.Frame(contenido, bg="#F5F5F5")
        titulo_frame.pack(fill="x", pady=(0, 8))

        tk.Label(titulo_frame, text=f"Cliente: ", bg="#F5F5F5", fg="#666666",
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(titulo_frame, text=f"{solicitud.cliente}", bg="#F5F5F5", fg="#222222",
                 font=("Segoe UI", 11, "bold")).pack(side="left", padx=(0, 15))

        tk.Label(titulo_frame, text=f"Aparato/Clase: ", bg="#F5F5F5", fg="#666666",
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(titulo_frame, text=f"{solicitud.aparato}", bg="#F5F5F5", fg="#2196F3",
                 font=("Segoe UI", 11, "bold")).pack(side="left")

        # Segunda fila: Hora y Estado
        info_frame = tk.Frame(contenido, bg="#F5F5F5")
        info_frame.pack(fill="x", pady=(0, 10))

        tk.Label(info_frame, text=f"Hora: ", bg="#F5F5F5", fg="#666666",
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(info_frame, text=f"{solicitud.hora}", bg="#F5F5F5", fg="#222222",
                 font=("Segoe UI", 10)).pack(side="left", padx=(0, 15))

        tk.Label(info_frame, text=f"Estado: ", bg="#F5F5F5", fg="#666666",
                 font=("Segoe UI", 10, "bold")).pack(side="left")

        estado_color = "#FF9800" if solicitud.estado.lower() == "pendiente" else "#4CAF50"
        tk.Label(info_frame, text=f"{solicitud.estado}", bg="#F5F5F5", fg=estado_color,
                 font=("Segoe UI", 10, "bold")).pack(side="left")

        # Botones
        botones_frame = tk.Frame(contenido, bg="#F5F5F5")
        botones_frame.pack(fill="x", pady=(5, 0))

        btn_aceptar = tk.Button(botones_frame, text="✓ Aceptar", bg="#4CAF50", fg="white",
                               font=("Segoe UI", 10, "bold"), relief="flat", padx=12, pady=6,
                               command=lambda: self.aceptar_reserva(solicitud))
        btn_aceptar.pack(side="left", padx=(0, 10))

        btn_rechazar = tk.Button(botones_frame, text="✕ Rechazar", bg="#F44336", fg="white",
                                font=("Segoe UI", 10, "bold"), relief="flat", padx=12, pady=6,
                                command=lambda: self.rechazar_reserva(solicitud))
        btn_rechazar.pack(side="left")

        # Efecto hover
        def on_enter(e):
            tarjeta_frame.configure(bg="#EEEEEE")
            contenido.configure(bg="#EEEEEE")
            titulo_frame.configure(bg="#EEEEEE")
            info_frame.configure(bg="#EEEEEE")
            botones_frame.configure(bg="#EEEEEE")

        def on_leave(e):
            tarjeta_frame.configure(bg="#F5F5F5")
            contenido.configure(bg="#F5F5F5")
            titulo_frame.configure(bg="#F5F5F5")
            info_frame.configure(bg="#F5F5F5")
            botones_frame.configure(bg="#F5F5F5")

        tarjeta_frame.bind("<Enter>", on_enter)
        tarjeta_frame.bind("<Leave>", on_leave)

    def aceptar_reserva(self, solicitud):
        if solicitud:
            self.servicio_reservas.aceptar_reserva(solicitud)
            nombre = solicitud.aparato.lower()

            # Determinar si es aparato o clase
            aparatos = [a.nombre.lower() for a in self.servicio_aparatos.listar_aparatos()]
            clases = [c.nombre.lower() for c in self.servicio_clases.listar_clases()]

            if nombre in aparatos:
                # Marcar aparato ocupado 30 min
                self.servicio_aparatos.marcar_ocupado_por_nombre(nombre, minutos=30, cliente=solicitud.cliente)
            elif nombre in clases:
                # Marcar clase ocupada 30 min
                self.servicio_clases.marcar_ocupado(nombre, minutos=30, cliente=solicitud.cliente)

            self.cargar_notificaciones()

    def rechazar_reserva(self, solicitud):
        if solicitud:
            self.servicio_reservas.denegar_reserva(solicitud)
            self.cargar_notificaciones()
