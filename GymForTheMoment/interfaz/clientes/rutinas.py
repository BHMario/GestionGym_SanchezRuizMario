import tkinter as tk
from tkinter import ttk
from utilidades.ui import set_uniform_window

def aclarar_color(hex_color, factor=0.2):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02X}{g:02X}{b:02X}"

class VentanaRutinas:
    def __init__(self, root):
        self.root = root
        self.root.title("Rutinas - Gym For The Moment")
        set_uniform_window(self.root, width_frac=0.7, height_frac=0.75, min_width=1000, min_height=700)
        self.root.configure(bg="#FFFFFF")

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

        tk.Label(self.root, text="Seleccione su Rutina", bg="#FFFFFF", fg="#444444",
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

        self.rutinas = [
            {
                "nombre": "Rutina Full Body",
                "descripcion": "Entrenamiento completo para todo el cuerpo.",
                "ejercicios": [
                    {"nombre": "Sentadillas", "series": 3, "repeticiones": 12, "descanso": "60s"},
                    {"nombre": "Press de banca", "series": 3, "repeticiones": 10, "descanso": "90s"},
                    {"nombre": "Remo con mancuerna", "series": 3, "repeticiones": 12, "descanso": "60s"}
                ]
            },
            {
                "nombre": "Rutina Cardio",
                "descripcion": "Ejercicios cardiovasculares para quemar grasa.",
                "ejercicios": [
                    {"nombre": "Cinta de correr", "series": 1, "repeticiones": "30 min", "descanso": "0s"},
                    {"nombre": "Elíptica", "series": 1, "repeticiones": "20 min", "descanso": "0s"},
                ]
            },
            {
                "nombre": "Rutina Fuerza",
                "descripcion": "Rutina centrada en aumentar la fuerza muscular.",
                "ejercicios": [
                    {"nombre": "Peso muerto", "series": 4, "repeticiones": 8, "descanso": "120s"},
                    {"nombre": "Dominadas", "series": 3, "repeticiones": 10, "descanso": "90s"},
                ]
            },
            {
                "nombre": "Rutina Yoga",
                "descripcion": "Ejercicios de yoga para flexibilidad y relajación.",
                "ejercicios": [
                    {"nombre": "Saludos al sol", "series": 3, "repeticiones": 5, "descanso": "30s"},
                    {"nombre": "Postura del guerrero", "series": 2, "repeticiones": 1, "descanso": "30s"}
                ]
            },
            {
                "nombre": "Rutina HIIT",
                "descripcion": "Entrenamiento de alta intensidad por intervalos.",
                "ejercicios": [
                    {"nombre": "Burpees", "series": 4, "repeticiones": 15, "descanso": "30s"},
                    {"nombre": "Jumping Jacks", "series": 4, "repeticiones": 20, "descanso": "30s"},
                ]
            },
            {
                "nombre": "Rutina Piernas",
                "descripcion": "Rutina enfocada en tren inferior.",
                "ejercicios": [
                    {"nombre": "Prensa de piernas", "series": 4, "repeticiones": 12, "descanso": "60s"},
                    {"nombre": "Zancadas", "series": 3, "repeticiones": 15, "descanso": "60s"},
                ]
            },
        ]

        self._cargar_tarjetas_rutinas()

    def _on_mousewheel_limited(self, event):
        delta = int(-1 * (event.delta / 120) * 30)
        y1, y2 = self.canvas.yview()
        if (delta < 0 and y1 <= 0) or (delta > 0 and y2 >= 1):
            return
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _cargar_tarjetas_rutinas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        filas = (len(self.rutinas) + 2) // 3
        index = 0
        color_base = "#64B5F6"

        for fila in range(filas):
            row_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
            row_frame.pack(expand=True, fill="both", pady=10)

            for col in range(3):
                if index >= len(self.rutinas):
                    break

                rutina = self.rutinas[index]
                tarjeta = tk.Frame(row_frame, bg=color_base, width=200, height=200, bd=0)
                tarjeta.pack(side="left", padx=20, expand=True, fill="both")
                tarjeta.pack_propagate(False)

                nombre_label = tk.Label(tarjeta, text=rutina["nombre"], bg=color_base, fg="white",
                                        font=("Segoe UI", 14, "bold"), wraplength=180, justify="center")
                nombre_label.pack(expand=True, fill="both")

                tk.Button(tarjeta, text="Ver Detalle", bg="#FFFFFF", fg="#222222",
                          font=("Segoe UI", 12, "bold"), bd=0,
                          command=lambda r=rutina: self._detalle_rutina(r)).pack(fill="x", padx=10, pady=10)

                tarjeta.bind("<Enter>", lambda e, t=tarjeta, l=nombre_label, c=color_base:
                             (t.configure(bg=aclarar_color(c, 0.3)), l.configure(bg=aclarar_color(c, 0.3))))
                tarjeta.bind("<Leave>", lambda e, t=tarjeta, l=nombre_label, c=color_base:
                             (t.configure(bg=c), l.configure(bg=c)))

                index += 1

    def _detalle_rutina(self, rutina):
        ventana_detalle = tk.Toplevel(self.root)
        ventana_detalle.title(rutina["nombre"])
        set_uniform_window(ventana_detalle, width_frac=0.45, height_frac=0.6, min_width=520, min_height=480)
        ventana_detalle.configure(bg="#FFFFFF")

        tk.Button(ventana_detalle, text="← Volver", bg="#333333", fg="white",
                  font=("Segoe UI", 12, "bold"), command=ventana_detalle.destroy).pack(anchor="nw", padx=20, pady=20)

        tk.Label(ventana_detalle, text=rutina["nombre"], bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 20, "bold")).pack(pady=20)

        tk.Label(ventana_detalle, text=rutina["descripcion"], bg="#FFFFFF", fg="#444444",
                 font=("Segoe UI", 12), wraplength=450, justify="left").pack(pady=10)

        for ex in rutina.get("ejercicios", []):
            texto = f"{ex['nombre']} - Series: {ex['series']}, Reps: {ex['repeticiones']}, Descanso: {ex['descanso']}"
            tk.Label(ventana_detalle, text=texto, bg="#FFFFFF", fg="#555555",
                     font=("Segoe UI", 12), wraplength=450, justify="left").pack(anchor="w", padx=20, pady=2)
