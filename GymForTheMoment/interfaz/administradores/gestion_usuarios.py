import tkinter as tk
from tkinter import ttk
from servicios.servicio_clientes import ServicioClientes
from modelos.cliente import Cliente

def aclarar_color(hex_color, factor=0.2):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02X}{g:02X}{b:02X}"

class VentanaGestionUsuarios:
    def __init__(self, root, refresco_periodico_ms=2000):
        self.root = root
        self.root.title("Gestión de Usuarios - Gym For The Moment")
        self.root.geometry("900x700")
        self.root.configure(bg="#FFFFFF")
        self.servicio_clientes = ServicioClientes()

        self.refresco_periodico_ms = refresco_periodico_ms

        self._configurar_estilos()
        self._construir_interfaz()
        self._programar_refresco()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#FFFFFF", foreground="#222222", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 12, "bold"))
        style.configure("Tarjeta.TFrame", background="#F5F5F5", relief="ridge", borderwidth=2)

    def _construir_interfaz(self):
        # Header con título y botón de refrescar
        header_frame = tk.Frame(self.root, bg="#FFFFFF")
        header_frame.pack(pady=15, padx=20, fill="x")

        tk.Label(header_frame, text="Listado de Clientes", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(side="left", expand=True)

        tk.Button(header_frame, text="Refrescar Usuarios", bg="#64B5F6", fg="white",
                  font=("Segoe UI", 11, "bold"), command=self._cargar_usuarios_tarjetas,
                  relief="flat", padx=15, pady=8).pack(side="right")

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


        self._cargar_usuarios_tarjetas()

    def _on_mousewheel_limited(self, event):
        delta = int(-1 * (event.delta / 120) * 30)
        y1, y2 = self.canvas.yview()
        if (delta < 0 and y1 <= 0) or (delta > 0 and y2 >= 1):
            return
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _cargar_usuarios_tarjetas(self):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()

        clientes_dict = self.servicio_clientes.listar_clientes_bd()

        clientes = [Cliente(id=None, usuario=c["usuario"], email=c["email"],
                            contrasena="", pagado=bool(c["pagado"]), rol=c["rol"]) for c in clientes_dict]

        if not clientes:
            tk.Label(self.scrollable_frame, text="No hay clientes registrados", bg="#FFFFFF",
                     fg="#444444", font=("Segoe UI", 12)).pack(pady=20)
            return

        filas = (len(clientes) + 2) // 3
        index = 0

        for fila in range(filas):
            row_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
            row_frame.pack(expand=True, fill="both", pady=10)
            for col in range(3):
                if index >= len(clientes):
                    break
                cliente = clientes[index]
                tarjeta = ttk.Frame(row_frame, style="Tarjeta.TFrame", width=260, height=140)
                tarjeta.pack(side="left", padx=15, expand=True, fill="both")
                tarjeta.pack_propagate(False)

                tk.Label(tarjeta, text=f"{cliente.usuario}", bg="#F5F5F5", fg="#222222",
                         font=("Segoe UI", 14, "bold")).pack(pady=(10, 5))
                tk.Label(tarjeta, text=f"{cliente.email}", bg="#F5F5F5", fg="#444444",
                         font=("Segoe UI", 12)).pack(pady=(0, 6))

                estado_color = "#4CAF50" if cliente.pagado else "#F44336"
                estado_texto = "Pagado" if cliente.pagado else "Moroso"
                tk.Label(tarjeta, text=f"Estado: {estado_texto}", bg="#F5F5F5",
                         fg=estado_color, font=("Segoe UI", 12, "bold")).pack(pady=(0, 8))

                index += 1

    def _programar_refresco(self):
        try:
            self._cargar_usuarios_tarjetas()
        except Exception:
            pass
        self.root.after(self.refresco_periodico_ms, self._programar_refresco)
