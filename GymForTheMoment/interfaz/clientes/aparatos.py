import tkinter as tk
from tkinter import ttk
from servicios.servicio_aparatos import ServicioAparatos
from servicios.servicio_reservas import ServicioReservas

def aclarar_color(hex_color, factor=0.2):
    """Aclara un color hexadecimal"""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02X}{g:02X}{b:02X}"

class VentanaAparatos:
    def __init__(self, root):
        self.root = root
        self.root.title("Aparatos - Gym For The Moment")
        self.root.geometry("1000x700")
        self.root.configure(bg="#FFFFFF")
        self.servicio_aparatos = ServicioAparatos()
        self.servicio_reservas = ServicioReservas()  # Para notificaciones

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

        # Canvas + Scrollbar
        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window_id, width=e.width))
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Scroll limitado
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
        aparatos = self.servicio_aparatos.listar_aparatos()
        filas = (len(aparatos) + 2) // 3
        index = 0

        color_musculo = {
            "cuádriceps": "#FF8A65",
            "isquiotibiales": "#4DB6AC",
            "pecho": "#F06292",
            "hombros": "#BA68C8",
            "espalda": "#64B5F6",
            "cardio": "#81C784",
            "abductores": "#FFD54F",
            "aductores": "#A1887F",
            "otros": "#90A4AE"
        }

        for fila in range(filas):
            row_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
            row_frame.pack(expand=True, fill="both", pady=10)

            for col in range(3):
                if index >= len(aparatos):
                    break

                aparato = aparatos[index]

                nombre = aparato.nombre.lower()
                if "cuádriceps" in nombre:
                    color_base = color_musculo["cuádriceps"]
                elif "curl femoral" in nombre:
                    color_base = color_musculo["isquiotibiales"]
                elif "press banca" in nombre or "pectoral" in nombre:
                    color_base = color_musculo["pecho"]
                elif "militar" in nombre:
                    color_base = color_musculo["hombros"]
                elif "remo" in nombre or "dorsalera" in nombre:
                    color_base = color_musculo["espalda"]
                elif "elíptica" in nombre or "bicicleta" in nombre or "cinta" in nombre:
                    color_base = color_musculo["cardio"]
                elif "abductor" in nombre:
                    color_base = color_musculo["abductores"]
                elif "aductor" in nombre:
                    color_base = color_musculo["aductores"]
                else:
                    color_base = color_musculo["otros"]

                tarjeta = tk.Frame(row_frame, bg=color_base, width=200, height=300, bd=0, relief="ridge")
                tarjeta.pack(side="left", padx=20, expand=True, fill="both")
                tarjeta.pack_propagate(False)

                # Label del nombre
                nombre_label = tk.Label(tarjeta, text=aparato.nombre, bg=color_base, fg="white",
                                        font=("Segoe UI", 14, "bold"), wraplength=180, justify="center")
                nombre_label.pack(expand=True, fill="both")

                # Botón detalle
                tk.Button(tarjeta, text="Ver Detalle / Reservar", bg="#FFFFFF", fg="#222222",
                          font=("Segoe UI", 12, "bold"), bd=0,
                          command=lambda a=aparato: self._detalle_aparato(a)).pack(expand=False, fill="x", padx=10, pady=10)

                # Hover: cambiar color de tarjeta y label simultáneamente
                def on_enter(e, t=tarjeta, l=nombre_label, c=color_base):
                    hover_color = aclarar_color(c, 0.3)
                    t.configure(bg=hover_color)
                    l.configure(bg=hover_color)

                def on_leave(e, t=tarjeta, l=nombre_label, c=color_base):
                    t.configure(bg=c)
                    l.configure(bg=c)

                tarjeta.bind("<Enter>", on_enter)
                tarjeta.bind("<Leave>", on_leave)

                index += 1

    # ----------------------
    # Detalles de aparato con Toplevel y mensaje de notificación
    # ----------------------
    def _detalle_aparato(self, aparato):
        ventana_detalle = tk.Toplevel(self.root)
        ventana_detalle.title(f"{aparato.nombre} - Detalle")
        ventana_detalle.geometry("500x450")
        ventana_detalle.configure(bg="#FFFFFF")

        # Botón volver
        tk.Button(ventana_detalle, text="← Volver", bg="#333333", fg="white",
                  font=("Segoe UI", 12, "bold"), command=ventana_detalle.destroy).pack(anchor="nw", padx=20, pady=20)

        tk.Label(ventana_detalle, text=aparato.nombre, bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 20, "bold")).pack(pady=20)
        tk.Label(ventana_detalle, text=f"{aparato.descripcion}", bg="#FFFFFF", fg="#444444",
                 font=("Segoe UI", 12), justify="left", wraplength=450).pack(pady=10)
        tk.Label(ventana_detalle, text=f"Estado: {'Libre' if not aparato.ocupado else 'Ocupado'}",
                 bg="#FFFFFF", fg="#444444", font=("Segoe UI", 12, "bold")).pack(pady=10)

        # Label para mostrar mensaje de reserva
        msg_reserva = tk.Label(ventana_detalle, text="", bg="#FFFFFF", fg="green",
                               font=("Segoe UI", 12, "bold"))
        msg_reserva.pack(pady=10)

        # Botón solicitar reserva
        tk.Button(ventana_detalle, text="Solicitar Reserva", bg="#64B5F6", fg="white",
                  font=("Segoe UI", 12, "bold"),
                  command=lambda: self._solicitar_reserva(aparato, msg_reserva)).pack(pady=20)

    def _solicitar_reserva(self, aparato, msg_label):
        # Crear la reserva en la base de datos
        # Aquí asumimos que tenemos un cliente logueado, por ejemplo "usuario1"
        cliente_actual = "usuario1"  # Cambiar según tu sistema de login
        import datetime
        hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.servicio_reservas.crear_reserva(cliente_actual, aparato.nombre, hora_actual)

        # Mostrar mensaje al cliente
        msg_label.config(text=f"Su solicitud para '{aparato.nombre}' ha sido enviada al administrador", fg="green")
        print(f"Notificación: Solicitud de reserva para '{aparato.nombre}' enviada al administrador")
