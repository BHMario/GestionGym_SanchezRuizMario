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
        header = tk.Frame(self.root, bg="#FFFFFF")
        header.pack(fill="x", pady=20, padx=20)

        tk.Label(header, text="Gestión de Recibos", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(side="left")

        acciones = tk.Frame(header, bg="#FFFFFF")
        acciones.pack(side="right")

        tk.Button(acciones, text="Generar Recibos Mensuales", bg="#64B5F6", fg="white",
                  font=("Segoe UI", 12, "bold"), command=self.generar_recibos, relief="flat", padx=12, pady=6).pack(side="left", padx=8)

        tk.Button(acciones, text="Ver Clientes Morosos", bg="#F06292", fg="white",
                  font=("Segoe UI", 12, "bold"), command=self.ver_morosos, relief="flat", padx=12, pady=6).pack(side="left")

        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window_id, width=e.width))
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

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

        for cliente in morosos:
            tarjeta = tk.Frame(self.scrollable_frame, bg="#F0F7FF", width=640, height=60, bd=1, relief="solid")
            tarjeta.pack(pady=6, padx=10, fill="x")
            tarjeta.pack_propagate(False)

            contenido = tk.Frame(tarjeta, bg="#F0F7FF")
            contenido.pack(fill="both", expand=True, padx=12, pady=6)

            tk.Label(contenido, text=f"{cliente.usuario}", bg="#F0F7FF", fg="#222222",
                     font=("Segoe UI", 12, "bold")).pack(side="left")
            tk.Label(contenido, text=f"{cliente.email}", bg="#F0F7FF", fg="#444444",
                     font=("Segoe UI", 12)).pack(side="left", padx=10)

            # Hover
            def _on_enter(e, f=tarjeta, c=contenido):
                f.configure(bg="#E3F2FD")
                c.configure(bg="#E3F2FD")

            def _on_leave(e, f=tarjeta, c=contenido):
                f.configure(bg="#F0F7FF")
                c.configure(bg="#F0F7FF")

            tarjeta.bind("<Enter>", _on_enter)
            tarjeta.bind("<Leave>", _on_leave)
