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
                  font=("Segoe UI", 12, "bold"), command=self.ver_morosos, relief="flat", padx=12, pady=6).pack(side="left", padx=8)
        
        tk.Button(acciones, text="Resumen de Cobranza", bg="#81C784", fg="white",
                  font=("Segoe UI", 12, "bold"), command=self.ver_resumen_cobranza, relief="flat", padx=12, pady=6).pack(side="left")

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
        # Mostrar morosos basados en la tabla 'recibos' para el mes actual
        morosos_usernames = self.servicio_recibos.listar_morosos()

        if not morosos_usernames:
            tk.Label(self.scrollable_frame, text="No hay clientes morosos (según recibos del mes)", bg="#FFFFFF",
                     fg="#444444", font=("Segoe UI", 12, "bold")).pack(pady=10)
            return

        tk.Label(self.scrollable_frame, text="Clientes Morosos (según recibos)", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        for username in morosos_usernames:
            cliente = self.servicio_clientes.obtener_cliente_por_usuario(username)
            if not cliente:
                continue

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

    def ver_resumen_cobranza(self):
        """Muestra un resumen exacto de cobranza del mes actual"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        resumen = self.servicio_recibos.obtener_resumen_cobranza()
        
        # Título
        tk.Label(self.scrollable_frame, text="Resumen de Cobranza", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 16, "bold")).pack(pady=15)
        
        # Tarjeta de resumen
        tarjeta_resumen = tk.Frame(self.scrollable_frame, bg="#E8F5E9", bd=2, relief="solid")
        tarjeta_resumen.pack(pady=10, padx=20, fill="x")
        
        contenido_resumen = tk.Frame(tarjeta_resumen, bg="#E8F5E9")
        contenido_resumen.pack(padx=20, pady=15, fill="both")
        
        tk.Label(contenido_resumen, text=f"Mes: {resumen['mes']}", bg="#E8F5E9", fg="#222222",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=5)
        
        tk.Label(contenido_resumen, text=f"Total de Clientes: {resumen['total_clientes']}", bg="#E8F5E9", 
                 fg="#444444", font=("Segoe UI", 12)).pack(anchor="w", pady=3)
        
        tk.Label(contenido_resumen, text=f"✓ Pagados: {resumen['pagados']}", bg="#E8F5E9", 
                 fg="#2E7D32", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=3)
        
        tk.Label(contenido_resumen, text=f"✗ Morosos: {resumen['morosos']}", bg="#E8F5E9", 
                 fg="#C62828", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=3)
        
        # Barra de progreso visual
        barra_frame = tk.Frame(contenido_resumen, bg="#CCCCCC", height=20)
        barra_frame.pack(fill="x", pady=10)
        barra_frame.pack_propagate(False)
        
        porcentaje = resumen['porcentaje_cobranza']
        barra_pagada = tk.Frame(barra_frame, bg="#4CAF50", height=20)
        barra_pagada.place(relwidth=porcentaje/100, relheight=1)
        
        tk.Label(contenido_resumen, text=f"Cobranza: {resumen['porcentaje_cobranza']}%", bg="#E8F5E9", 
                 fg="#1B5E20", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=5)
        
        # Detalles de morosos
        tk.Label(self.scrollable_frame, text="Detalles de Morosos", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 14, "bold")).pack(pady=15, anchor="w", padx=20)
        
        morosos_detalles = self.servicio_recibos.obtener_morosos_con_detalles()
        
        if not morosos_detalles:
            tk.Label(self.scrollable_frame, text="✓ Sin morosos este mes", bg="#FFFFFF", fg="#2E7D32",
                     font=("Segoe UI", 12, "bold")).pack(pady=10)
        else:
            for moroso in morosos_detalles:
                tarjeta = tk.Frame(self.scrollable_frame, bg="#FFEBEE", bd=1, relief="solid")
                tarjeta.pack(pady=6, padx=20, fill="x")
                tarjeta.pack_propagate(False)
                
                contenido = tk.Frame(tarjeta, bg="#FFEBEE")
                contenido.pack(fill="both", expand=True, padx=12, pady=8)
                
                tk.Label(contenido, text=moroso['usuario'], bg="#FFEBEE", fg="#222222",
                         font=("Segoe UI", 11, "bold")).pack(anchor="w")
                tk.Label(contenido, text=moroso['email'], bg="#FFEBEE", fg="#666666",
                         font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 0))
                tk.Label(contenido, text=f"Generado: {moroso['fecha_generacion']}", bg="#FFEBEE", 
                         fg="#888888", font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))

