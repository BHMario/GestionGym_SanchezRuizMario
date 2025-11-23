import tkinter as tk
from tkinter import ttk
from servicios.servicio_recibos import ServicioRecibos
from servicios.servicio_clientes import ServicioClientes  # ← IMPORTANTE


class VentanaGestionRecibos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Recibos - Gym For The Moment")
        self.root.geometry("700x500")
        self.root.configure(bg="#FFFFFF")

        self.servicio_recibos = ServicioRecibos()
        self.servicio_clientes = ServicioClientes()  # ← NUEVO: para consultar morosos reales

        self._configurar_estilos()
        self._construir_interfaz()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#F5F5F5", foreground="#222222", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 12, "bold"))

    def _construir_interfaz(self):
        tk.Label(self.root, text="Gestión de Recibos", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(pady=20)

        tk.Button(self.root, text="Generar Recibos Mensuales", bg="#64B5F6", fg="white",
                  font=("Segoe UI", 12, "bold"), command=self.generar_recibos).pack(pady=10)

        tk.Button(self.root, text="Ver Clientes Morosos", bg="#F06292", fg="white",
                  font=("Segoe UI", 12, "bold"), command=self.ver_morosos).pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window_id, width=e.width))
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def generar_recibos(self):
        self.servicio_recibos.generar_recibos_mes()

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text="Recibos generados correctamente ✅",
                 bg="#FFFFFF", fg="green", font=("Segoe UI", 12, "bold")).pack(pady=10)

    def ver_morosos(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # ⬇️ CAMBIO: Ahora se consultan los morosos reales desde la tabla CLIENTES
        morosos = [c for c in self.servicio_clientes.listar_clientes() if not c.pagado]

        if not morosos:
            tk.Label(self.scrollable_frame, text="No hay clientes morosos", bg="#FFFFFF",
                     fg="#444444", font=("Segoe UI", 12, "bold")).pack(pady=10)
            return

        tk.Label(self.scrollable_frame, text="Clientes Morosos", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        color_base = "#F06292"
        for cliente in morosos:
            tarjeta = tk.Frame(self.scrollable_frame, bg=color_base, width=600, height=50, bd=0)
            tarjeta.pack(pady=5, padx=10, fill="x")
            tarjeta.pack_propagate(False)

            tk.Label(tarjeta, text=f"{cliente.usuario} - {cliente.email}", bg=color_base, fg="white",
                     font=("Segoe UI", 12, "bold")).pack(expand=True, fill="both")
