import tkinter as tk
from tkinter import ttk
from servicios.servicio_clases import ServicioClases
from servicios.servicio_reservas import ServicioReservas
import datetime

def aclarar_color(hex_color, factor=0.2):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02X}{g:02X}{b:02X}"

class VentanaClases:
    def __init__(self, root, cliente_actual="usuario1"):
        self.root = root
        self.root.title("Clases - Gym For The Moment")
        self.root.geometry("1000x700")
        self.root.configure(bg="#FFFFFF")

        self.cliente_actual = cliente_actual  # ← ahora el cliente aparece en la notificación

        self.servicio_clases = ServicioClases()
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

        tk.Label(self.root, text="Listado de Clases Disponibles", bg="#FFFFFF", fg="#444444",
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
        self._cargar_clases_tarjetas()

    def _on_mousewheel_limited(self, event):
        delta = int(-1 * (event.delta / 120) * 30)
        y1, y2 = self.canvas.yview()
        if (delta < 0 and y1 <= 0) or (delta > 0 and y2 >= 1):
            return
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _cargar_clases_tarjetas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        clases = self.servicio_clases.listar_clases()
        filas = (len(clases) + 2) // 3
        index = 0

        color_tipo = {"Relax": "#81C784", "Fuerza": "#F06292", "Cardio": "#64B5F6", "otros": "#90A4AE"}

        for fila in range(filas):
            row_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
            row_frame.pack(expand=True, fill="both", pady=10)

            for col in range(3):
                if index >= len(clases):
                    break

                clase = clases[index]
                tipo = clase.tipo if clase.tipo in color_tipo else "otros"
                color_base = color_tipo[tipo]

                tarjeta = tk.Frame(row_frame, bg=color_base, width=200, height=300, bd=0)
                tarjeta.pack(side="left", padx=20, expand=True, fill="both")
                tarjeta.pack_propagate(False)

                nombre_label = tk.Label(tarjeta, text=clase.nombre, bg=color_base, fg="white",
                                        font=("Segoe UI", 14, "bold"), wraplength=180, justify="center")
                nombre_label.pack(expand=True, fill="both")

                tk.Button(tarjeta, text="Ver Detalle / Reservar", bg="#FFFFFF", fg="#222222",
                          font=("Segoe UI", 12, "bold"), bd=0,
                          command=lambda c=clase: self._detalle_clase(c)).pack(fill="x", padx=10, pady=10)

                tarjeta.bind("<Enter>", lambda e, t=tarjeta, l=nombre_label, c=color_base:
                             (t.configure(bg=aclarar_color(c, 0.3)), l.configure(bg=aclarar_color(c, 0.3))))

                tarjeta.bind("<Leave>", lambda e, t=tarjeta, l=nombre_label, c=color_base:
                             (t.configure(bg=c), l.configure(bg=c)))

                index += 1

    def _detalle_clase(self, clase):
        ventana_detalle = tk.Toplevel(self.root)
        ventana_detalle.title(f"{clase.nombre} - Detalle")
        ventana_detalle.geometry("500x450")
        ventana_detalle.configure(bg="#FFFFFF")

        tk.Button(ventana_detalle, text="← Volver", bg="#333333", fg="white",
                  font=("Segoe UI", 12, "bold"), command=ventana_detalle.destroy).pack(anchor="nw", padx=20, pady=20)

        tk.Label(ventana_detalle, text=clase.nombre, bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 20, "bold")).pack(pady=20)

        tk.Label(ventana_detalle, text=f"{clase.descripcion}", bg="#FFFFFF", fg="#444444",
                 font=("Segoe UI", 12), justify="left", wraplength=450).pack(pady=10)

        estado_label = tk.Label(ventana_detalle,
                                text=f"Estado: {'Libre' if not clase.ocupado else 'Ocupado'}",
                                bg="#FFFFFF", fg="#444444", font=("Segoe UI", 12, "bold"))
        estado_label.pack(pady=10)

        msg_reserva = tk.Label(ventana_detalle, text="", bg="#FFFFFF", fg="green",
                               font=("Segoe UI", 12, "bold"))
        msg_reserva.pack(pady=10)

        tk.Button(ventana_detalle, text="Solicitar Reserva", bg="#64B5F6", fg="white",
                  font=("Segoe UI", 12, "bold"),
                  command=lambda: self._solicitar_reserva(clase, msg_reserva, estado_label)).pack(pady=20)

        # 🔄 Actualizar estado cada segundo
        self._actualizar_estado_periodico(clase, estado_label, ventana_detalle)

    def _actualizar_estado_periodico(self, clase, estado_label, ventana):
        if not ventana.winfo_exists():
            return

        clase_actualizada = self.servicio_clases.obtener_clase_por_nombre(clase.nombre)

        if clase_actualizada:
            estado_label.config(
                text=f"Estado: {'Libre' if not clase_actualizada.ocupado else 'Ocupado'}"
            )

        ventana.after(1000, lambda: self._actualizar_estado_periodico(clase, estado_label, ventana))

    def _solicitar_reserva(self, clase, msg_label, estado_label):
        hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ✔ ahora se muestra el cliente correcto al admin
        self.servicio_reservas.crear_reserva(self.cliente_actual, clase.nombre, hora_actual)

        msg_label.config(text=f"Su solicitud para '{clase.nombre}' ha sido enviada al administrador", fg="green")

        print(f"Notificación: Solicitud de reserva para '{clase.nombre}' enviada al administrador por {self.cliente_actual}")
