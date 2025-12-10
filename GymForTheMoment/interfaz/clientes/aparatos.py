import tkinter as tk
from tkinter import ttk
from servicios.servicio_aparatos import ServicioAparatos
from servicios.servicio_reservas import ServicioReservas
from utilidades.ui import set_uniform_window
import datetime

def aclarar_color(hex_color, factor=0.2):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02X}{g:02X}{b:02X}"

class VentanaAparatos:
    def __init__(self, root, cliente_actual=None):
        self.root = root
        self.root.title("Aparatos - Gym For The Moment")
        set_uniform_window(self.root, width_frac=0.7, height_frac=0.75, min_width=1000, min_height=700)
        self.root.configure(bg="#FFFFFF")
        self.cliente_actual = cliente_actual or "usuario1"

        self.servicio_aparatos = ServicioAparatos()
        self.servicio_reservas = ServicioReservas()

        self._configurar_estilos()
        self._construir_interfaz()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#F5F5F5", foreground="#222222", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 12, "bold"))

    def _construir_interfaz(self):
        tk.Label(self.root, text="GYM FOR THE MOMENT", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(pady=(30, 10))
        tk.Label(self.root, text="Listado de Aparatos Disponibles", bg="#FFFFFF", fg="#444444",
                 font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

        tk.Button(self.root, text="Volver al Menú", bg="#333333", fg="white",
                  font=("Segoe UI", 12, "bold"), command=self.root.destroy).place(relx=0.95, rely=0.05, anchor="ne")

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

        self.root.update_idletasks()
        self._cargar_aparatos_tarjetas()

    def _on_mousewheel_limited(self, event):
        delta = int(-1 * (event.delta / 120) * 30)
        y1, y2 = self.canvas.yview()
        if (delta < 0 and y1 <= 0) or (delta > 0 and y2 >= 1):
            return
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _cargar_aparatos_tarjetas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        aparatos = self.servicio_aparatos.listar_aparatos()
        filas = (len(aparatos) + 2) // 3
        index = 0

        color_musculo = {
            "cuádriceps": "#FF8A65", "isquiotibiales": "#4DB6AC", "pecho": "#F06292",
            "hombros": "#BA68C8", "espalda": "#64B5F6", "cardio": "#81C784",
            "abductores": "#FFD54F", "aductores": "#A1887F", "otros": "#90A4AE"
        }

        for fila in range(filas):
            row_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
            row_frame.pack(expand=True, fill="both", pady=10)

            for col in range(3):
                if index >= len(aparatos):
                    break
                aparato = aparatos[index]
                nombre = aparato.nombre.lower()
                color_base = color_musculo["otros"]
                for key, color in color_musculo.items():
                    if key in nombre:
                        color_base = color
                        break

                tarjeta = tk.Frame(row_frame, bg=color_base, width=220, height=160, bd=0, relief="solid", highlightthickness=1, highlightbackground="#CCCCCC")
                tarjeta.pack(side="left", padx=15, pady=10, expand=True, fill="both")
                tarjeta.pack_propagate(False)

                nombre_label = tk.Label(tarjeta, text=aparato.nombre, bg=color_base, fg="white",
                                        font=("Segoe UI", 13, "bold"), wraplength=200, justify="center")
                nombre_label.pack(expand=True, fill="both", padx=10, pady=(15, 10))

                tk.Button(tarjeta, text="Ver Detalle / Reservar", bg="#FFFFFF", fg="#222222",
                          font=("Segoe UI", 10, "bold"), bd=0, relief="flat",
                          command=lambda a=aparato: self._detalle_aparato(a)).pack(fill="x", padx=8, pady=(5, 10))

                tarjeta.bind("<Enter>", lambda e, t=tarjeta, l=nombre_label, c=color_base:
                             (t.configure(bg=aclarar_color(c, 0.3)), l.configure(bg=aclarar_color(c, 0.3))))
                tarjeta.bind("<Leave>", lambda e, t=tarjeta, l=nombre_label, c=color_base:
                             (t.configure(bg=c), l.configure(bg=c)))
                nombre_label.bind("<Enter>", lambda e, t=tarjeta, l=nombre_label, c=color_base:
                                  (t.configure(bg=aclarar_color(c, 0.3)), l.configure(bg=aclarar_color(c, 0.3))))
                nombre_label.bind("<Leave>", lambda e, t=tarjeta, l=nombre_label, c=color_base:
                                  (t.configure(bg=c), l.configure(bg=c)))
                index += 1

    def _detalle_aparato(self, aparato):
        ventana_detalle = tk.Toplevel(self.root)
        ventana_detalle.title(f"{aparato.nombre} - Detalle")
        set_uniform_window(ventana_detalle, width_frac=0.4, height_frac=0.55, min_width=480, min_height=420)
        ventana_detalle.configure(bg="#FFFFFF")

        tk.Button(ventana_detalle, text="← Volver", bg="#333333", fg="white",
                  font=("Segoe UI", 12, "bold"), command=ventana_detalle.destroy).pack(anchor="nw", padx=20, pady=20)

        tk.Label(ventana_detalle, text=aparato.nombre, bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 20, "bold")).pack(pady=20)
        tk.Label(ventana_detalle, text=f"{aparato.descripcion}", bg="#FFFFFF", fg="#444444",
                 font=("Segoe UI", 12), justify="left", wraplength=450).pack(pady=10)

        estado_label = tk.Label(ventana_detalle,
                                text=f"Estado: {'Libre' if not aparato.ocupado else 'Ocupado'}",
                                bg="#FFFFFF", fg="#444444", font=("Segoe UI", 12, "bold"))
        estado_label.pack(pady=10)

        msg_reserva = tk.Label(ventana_detalle, text="", bg="#FFFFFF", fg="green",
                               font=("Segoe UI", 12, "bold"))
        msg_reserva.pack(pady=10)

        tk.Button(ventana_detalle, text="Solicitar Reserva", bg="#64B5F6", fg="white",
              font=("Segoe UI", 12, "bold"),
              command=lambda: self._abrir_dialogo_reserva(aparato, msg_reserva, estado_label)).pack(pady=20)

        self._actualizar_estado_periodico(aparato, estado_label, ventana_detalle)

    def _actualizar_estado_periodico(self, aparato, estado_label, ventana):
        if not ventana.winfo_exists():
            return

        aparato_actualizado = self.servicio_aparatos.obtener_aparato_por_nombre(aparato.nombre)
        if aparato_actualizado:
            estado_label.config(text=f"Estado: {'Libre' if not aparato_actualizado.ocupado else 'Ocupado'}")
        ventana.after(1000, lambda: self._actualizar_estado_periodico(aparato, estado_label, ventana))

    def _solicitar_reserva(self, aparato, msg_label, estado_label):
        # Este método queda para compatibilidad pero no se usa directamente
        raise NotImplementedError("Use el diálogo de selección de fecha/hora para reservar")

    def _abrir_dialogo_reserva(self, aparato, msg_label, estado_label):
        if aparato.ocupado:
            msg_label.config(text=f"Lo sentimos, '{aparato.nombre}' ya está ocupado.", fg="red")
            return

        import datetime as dt

        dlg = tk.Toplevel(self.root)
        dlg.title("Solicitar Reserva - Seleccione fecha y hora")
        set_uniform_window(dlg, width_frac=0.5, height_frac=0.75, min_width=550, min_height=500)
        dlg.configure(bg="#FFFFFF")

        tk.Label(dlg, text=f"Reservar: {aparato.nombre}", bg="#FFFFFF", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Frame para fecha con calendario (intenta usar tkcalendar, fallback a entrada manual)
        frame_fecha = tk.Frame(dlg, bg="#FFFFFF")
        frame_fecha.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_fecha, text="Seleccione fecha (L-V):", bg="#FFFFFF", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 5))
        
        date_entry = None
        try:
            from tkcalendar import DateEntry
            date_entry = DateEntry(frame_fecha, width=12, background="darkblue", foreground="white", borderwidth=2, year=dt.datetime.now().year, month=dt.datetime.now().month, day=dt.datetime.now().day)
            date_entry.pack(pady=5)
        except ImportError:
            # Fallback: entrada manual si tkcalendar no está instalado
            frame_entrada = tk.Frame(frame_fecha, bg="#FFFFFF")
            frame_entrada.pack(pady=5)
            tk.Label(frame_entrada, text="Formato YYYY-MM-DD:", bg="#FFFFFF", font=("Segoe UI", 9)).pack(side="left", padx=(0, 5))
            entry_fecha_manual = tk.Entry(frame_entrada, width=15)
            entry_fecha_manual.pack(side="left")
            entry_fecha_manual.insert(0, dt.datetime.now().strftime("%Y-%m-%d"))
            date_entry = entry_fecha_manual

        # Frame para horas en franjas de 30 minutos
        frame_horas = tk.Frame(dlg, bg="#FFFFFF")
        frame_horas.pack(pady=10, padx=20, fill="both", expand=True)

        tk.Label(frame_horas, text="Seleccione franja horaria (30 min):", bg="#FFFFFF", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))

        # Obtener las franjas disponibles para la fecha seleccionada
        def actualizar_franjas_disponibles(*args):
            # Limpiar franjas anteriores
            for widget in scrollable_horas.winfo_children():
                widget.destroy()
            frames_horas.clear()
            
            # Obtener fecha
            try:
                if hasattr(date_entry, 'get_date'):
                    fecha_obj = date_entry.get_date()
                    fecha_str = fecha_obj.strftime("%Y-%m-%d")
                else:
                    fecha_str = date_entry.get().strip()
                    fecha_obj = dt.datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except Exception:
                return
            
            # Obtener todas las franjas posibles con estado (libre/ocupada)
            try:
                franjas = self.servicio_reservas.generar_todas_horas_disponibles(aparato.nombre, fecha_str)
            except Exception:
                franjas = []
            
            # Generar UI para franjas con indicador visual
            for idx, franja in enumerate(franjas):
                h_inicio = int(franja['inicio'].split(":")[0])
                m_inicio = int(franja['inicio'].split(":")[1])
                franja_text = f"{franja['inicio']} - {franja['fin']}"
                
                # Color según estado
                if franja['estado'] == 'ocupada':
                    color_bg = "#FFEBEE"
                    color_text = "#C62828"
                    es_seleccionable = False
                    texto_extra = f" (Ocupado: {franja['cliente']})"
                else:
                    color_bg = "#E8F5E9"
                    color_text = "#2E7D32"
                    es_seleccionable = True
                    texto_extra = " (Libre)"
                
                # Frame para cada franja como tarjeta
                franja_frame = tk.Frame(scrollable_horas, bg=color_bg, relief="solid", bd=1)
                row = idx // 5
                col = idx % 5
                franja_frame.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
                
                if es_seleccionable:
                    # Radiobutton si está libre
                    rb = tk.Radiobutton(franja_frame, text=franja_text + texto_extra, variable=hora_seleccionada, 
                                       value=franja['inicio'], bg=color_bg, fg=color_text, font=("Segoe UI", 8, "bold"), 
                                       selectcolor="#64B5F6", activebackground="#C8E6C9", activeforeground="#1B5E20")
                    rb.pack(expand=True, fill="both", padx=8, pady=6)
                    
                    frames_horas.append({"frame": franja_frame, "rb": rb, "hora": franja['inicio']})
                else:
                    # Label si está ocupada (no seleccionable)
                    tk.Label(franja_frame, text=franja_text + texto_extra, bg=color_bg, fg=color_text, 
                            font=("Segoe UI", 7, "bold"), wraplength=80, justify="center").pack(expand=True, fill="both", padx=6, pady=4)
        
        # Canvas con scrollbar para las franjas
        canvas_horas = tk.Canvas(frame_horas, bg="#FFFFFF", highlightthickness=0, height=220)
        scrollbar_horas = tk.Scrollbar(frame_horas, orient="vertical", command=canvas_horas.yview)
        canvas_horas.configure(yscrollcommand=scrollbar_horas.set)
        canvas_horas.pack(side="left", fill="both", expand=True, pady=5)
        scrollbar_horas.pack(side="right", fill="y")

        scrollable_horas = tk.Frame(canvas_horas, bg="#FFFFFF")
        window_horas = canvas_horas.create_window((0, 0), window=scrollable_horas, anchor="nw")
        canvas_horas.bind("<Configure>", lambda e: canvas_horas.itemconfigure(window_horas, width=e.width))
        scrollable_horas.bind("<Configure>", lambda e: canvas_horas.configure(scrollregion=canvas_horas.bbox("all")))
        
        # Capturar scroll del canvas para no afectar ventana padre
        def _on_canvas_scroll(event):
            canvas_horas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas_horas.bind("<MouseWheel>", _on_canvas_scroll)

        hora_seleccionada = tk.StringVar()
        frames_horas = []
        
        # Actualizar franjas cuando cambia la fecha
        if hasattr(date_entry, 'bind'):
            date_entry.bind("<<Change>>", actualizar_franjas_disponibles)
        
        # Cargar franjas iniciales
        actualizar_franjas_disponibles()


        label_error = tk.Label(dlg, text="", bg="#FFFFFF", fg="red", font=("Segoe UI", 10))
        label_error.pack()

        def confirmar():
            hora = hora_seleccionada.get()

            if not hora:
                label_error.config(text="Debe seleccionar una franja horaria")
                return

            # Obtener fecha según el tipo de widget
            try:
                if hasattr(date_entry, 'get_date'):
                    # Es DateEntry (tkcalendar)
                    fecha_obj = date_entry.get_date()
                    fecha_str = fecha_obj.strftime("%Y-%m-%d")
                else:
                    # Es Entry manual
                    fecha_str = date_entry.get().strip()
                    fecha_obj = dt.datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except Exception as e:
                label_error.config(text=f"Formato de fecha inválido: {str(e)}")
                return

            # Validar que sea L-V
            if fecha_obj.weekday() > 4:
                label_error.config(text="Solo se permiten reservas de Lunes a Viernes")
                return

            datetime_str = f"{fecha_str} {hora}"
            try:
                self.servicio_reservas.crear_reserva(self.cliente_actual, aparato.nombre, datetime_str)
            except Exception as e:
                label_error.config(text=str(e))
                return
            msg_label.config(text=f"Su solicitud para '{aparato.nombre}' ha sido enviada al administrador", fg="green")
            print(f"Notificación: Solicitud de reserva para '{aparato.nombre}' enviada por {self.cliente_actual} para {datetime_str}")
            dlg.destroy()

        tk.Button(dlg, text="Confirmar Reserva", bg="#64B5F6", fg="white", font=("Segoe UI", 11, "bold"), command=confirmar).pack(pady=8)
        tk.Button(dlg, text="Cancelar", bg="#CCCCCC", command=dlg.destroy).pack(pady=4)
