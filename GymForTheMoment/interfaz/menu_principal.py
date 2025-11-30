import tkinter as tk
from interfaz.clientes.aparatos import VentanaAparatos
from interfaz.clientes.clases import VentanaClases
from interfaz.clientes.rutinas import VentanaRutinas
from interfaz.clientes.pagos import VentanaPagos

from interfaz.administradores.gestion_usuarios import VentanaGestionUsuarios
from interfaz.administradores.gestion_reservas import VentanaGestionReservas
from interfaz.administradores.gestion_recibos import VentanaGestionRecibos
from interfaz.administradores.notificaciones import VentanaNotificaciones

from utilidades.constantes import ROL_CLIENTE, ROL_ADMINISTRADOR
from utilidades.ui import set_uniform_window

class MenuPrincipal:
    def __init__(self, root, rol, nombre_usuario):
        self.root = root
        self.rol = rol
        self.nombre_usuario = nombre_usuario

        self.root.title("Gym For The Moment - Menú Principal")
        # Ventana principal uniformizada
        set_uniform_window(self.root, width_frac=0.7, height_frac=0.75, min_width=1000, min_height=700)
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.ventana_gestion_usuarios = None  # para callback

        self._construir_interfaz()

    def _construir_interfaz(self):
        tk.Label(self.root, text="GYM FOR THE MOMENT", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(pady=(30, 5))

        tk.Label(self.root, text=f"Bienvenido, {self.nombre_usuario}!", bg="#FFFFFF",
                 fg="#444444", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

        cerrar_sesion_btn = tk.Button(self.root, text="Cerrar Sesión", bg="#CC3333", fg="white",
                                      font=("Segoe UI", 12, "bold"), command=self._cerrar_sesion)
        cerrar_sesion_btn.place(relx=0.9, rely=0.05, anchor="ne")
        cerrar_sesion_btn.bind("<Enter>", lambda e: cerrar_sesion_btn.config(bg="#AA0000"))
        cerrar_sesion_btn.bind("<Leave>", lambda e: cerrar_sesion_btn.config(bg="#CC3333"))

        contenedor = tk.Frame(self.root, bg="#FFFFFF")
        contenedor.pack(expand=True, fill="both", pady=20, padx=50)

        if self.rol == ROL_CLIENTE:
            opciones = [
                ("Ver Aparatos", self.abrir_aparatos, "#FFB74D"),
                ("Ver Clases / Sesiones", self.abrir_clases, "#64B5F6"),
                ("Ver Rutinas", self.abrir_rutinas, "#81C784"),
                ("Pasarela de Pagos", self.abrir_pagos, "#BA68C8"),
            ]
        else:
            opciones = [
                ("Gestión de Usuarios", self.abrir_gestion_usuarios, "#64B5F6"),
                ("Gestión de Reservas", self.abrir_gestion_reservas, "#FFB74D"),
                ("Gestión de Recibos", self.abrir_gestion_recibos, "#81C784"),
                ("Notificaciones", self.abrir_notificaciones, "#BA68C8"),
            ]

        self._crear_tarjetas(contenedor, opciones)

        tk.Label(self.root, text="© 2025 Gym For The Moment", bg="#FFFFFF",
                 fg="#555555", font=("Segoe UI", 10)).pack(side="bottom", pady=10)

    def _crear_tarjetas(self, parent, opciones):
        filas = 2
        columnas = 2
        index = 0
        for fila in range(filas):
            row_frame = tk.Frame(parent, bg="#FFFFFF")
            row_frame.pack(expand=True, fill="both")
            for col in range(columnas):
                if index >= len(opciones):
                    break
                texto, comando, color = opciones[index]
                tarjeta = tk.Frame(row_frame, bg=color, width=200, height=120)
                tarjeta.pack(side="left", padx=20, pady=20, expand=True, fill="both")
                tarjeta.pack_propagate(False)
                btn = tk.Button(tarjeta, text=texto, bg=color, fg="white",
                                font=("Segoe UI", 14, "bold"), bd=0, command=comando)
                btn.pack(expand=True, fill="both")

                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#555555"))
                btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
                index += 1

    def _cerrar_sesion(self):
        self.root.destroy()
        from interfaz.login import Login
        root_login = tk.Tk()
        Login(root_login)
        root_login.mainloop()

    # VENTANAS SECUNDARIAS
    def abrir_aparatos(self):
        ventana = tk.Toplevel(self.root)
        set_uniform_window(ventana, width_frac=0.7, height_frac=0.75)
        VentanaAparatos(ventana, cliente_actual=self.nombre_usuario)

    def abrir_clases(self):
        ventana = tk.Toplevel(self.root)
        set_uniform_window(ventana, width_frac=0.7, height_frac=0.75)
        VentanaClases(ventana, cliente_actual=self.nombre_usuario)

    def abrir_rutinas(self):
        ventana = tk.Toplevel(self.root)
        set_uniform_window(ventana, width_frac=0.7, height_frac=0.75)
        VentanaRutinas(ventana)

    def abrir_pagos(self):
        ventana = tk.Toplevel(self.root)
        set_uniform_window(ventana, width_frac=0.7, height_frac=0.75)
        VentanaPagos(ventana, cliente_actual=self.nombre_usuario, callback_refrescar=self._refrescar_gestion_usuarios)

    def abrir_gestion_usuarios(self):
        self.ventana_gestion_usuarios = tk.Toplevel(self.root)
        set_uniform_window(self.ventana_gestion_usuarios, width_frac=0.7, height_frac=0.75)
        VentanaGestionUsuarios(self.ventana_gestion_usuarios)

    def abrir_gestion_reservas(self):
        ventana = tk.Toplevel(self.root)
        set_uniform_window(ventana, width_frac=0.75, height_frac=0.8)
        VentanaGestionReservas(ventana)

    def abrir_gestion_recibos(self):
        ventana = tk.Toplevel(self.root)
        set_uniform_window(ventana, width_frac=0.7, height_frac=0.75)
        VentanaGestionRecibos(ventana)

    def abrir_notificaciones(self):
        ventana = tk.Toplevel(self.root)
        set_uniform_window(ventana, width_frac=0.7, height_frac=0.75)
        VentanaNotificaciones(ventana)

    def _refrescar_gestion_usuarios(self):
        if self.ventana_gestion_usuarios and self.ventana_gestion_usuarios.winfo_exists():
            self.ventana_gestion_usuarios._cargar_usuarios_tarjetas()
