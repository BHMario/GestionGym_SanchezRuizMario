import tkinter as tk
from tkinter import ttk

# Submenús
from interfaz.clientes.aparatos import VentanaAparatos
from interfaz.clientes.clases import VentanaClases
from interfaz.clientes.rutinas import VentanaRutinas
from interfaz.clientes.pagos import VentanaPagos

from interfaz.administradores.gestion_usuarios import VentanaGestionUsuarios
from interfaz.administradores.gestion_reservas import VentanaGestionReservas
from interfaz.administradores.gestion_recibos import VentanaGestionRecibos
from interfaz.administradores.notificaciones import VentanaNotificaciones

from utilidades.constantes import ROL_CLIENTE, ROL_ADMINISTRADOR


class MenuPrincipal:
    def __init__(self, root, rol):
        self.root = root
        self.rol = rol

        # --- CONFIG VENTANA ---
        self.root.title("Gym For The Moment - Menú Principal")
        self.root.geometry("1000x700")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self._configurar_estilos()
        self._construir_interfaz()

    # ------------------------------
    #       ESTILOS TTK
    # ------------------------------
    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel",
                        background="#F5F5F5",
                        foreground="#222222",
                        font=("Segoe UI", 12))

        style.configure("TButton",
                        background="#333333",
                        foreground="#FFFFFF",
                        font=("Segoe UI", 12, "bold"),
                        padding=10)

        style.map("TButton",
                  background=[("active", "#555555")],
                  foreground=[("active", "white")])

    # ------------------------------
    #  CONSTRUCCIÓN DE INTERFAZ
    # ------------------------------
    def _construir_interfaz(self):

        # --- Sombra de tarjeta ---
        sombra = tk.Frame(self.root, bg="#CCCCCC")
        sombra.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

        # --- Tarjeta principal ---
        tarjeta = tk.Frame(self.root, bg="#F5F5F5")
        tarjeta.place(relx=0.5, rely=0.5, anchor="center", width=690, height=490)

        # Título
        tk.Label(tarjeta,
                 text="GYM FOR THE MOMENT",
                 bg="#F5F5F5",
                 fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(pady=(40, 10))

        tk.Label(tarjeta,
                 text=f"Menú Principal - Rol: {self.rol.upper()}",
                 bg="#F5F5F5",
                 fg="#444444",
                 font=("Segoe UI", 15, "bold")).pack(pady=(0, 30))

        # Contenedor de botones
        contenedor_botones = tk.Frame(tarjeta, bg="#F5F5F5")
        contenedor_botones.pack()

        # --- BOTONES SEGÚN ROL ---
        if self.rol == ROL_CLIENTE:
            self._construir_botones_cliente(contenedor_botones)
        elif self.rol == ROL_ADMINISTRADOR:
            self._construir_botones_admin(contenedor_botones)
        else:
            tk.Label(tarjeta, text="Rol desconocido", fg="red", bg="#F5F5F5").pack()

        # Pie de página
        tk.Label(tarjeta,
                 text="© 2025 Gym For The Moment",
                 bg="#F5F5F5",
                 fg="#555555",
                 font=("Segoe UI", 10)).pack(side="bottom", pady=20)

    # ------------------------------
    #       BOTONES CLIENTE
    # ------------------------------
    def _construir_botones_cliente(self, parent):
        opciones = [
            ("Ver Aparatos", self.abrir_aparatos),
            ("Ver Clases / Sesiones", self.abrir_clases),
            ("Ver Rutinas", self.abrir_rutinas),
            ("Pasarela de Pagos", self.abrir_pagos),
        ]

        for texto, comando in opciones:
            ttk.Button(parent, text=texto, command=comando).pack(fill="x", padx=150, pady=10)

    # ------------------------------
    #     BOTONES ADMINISTRADOR
    # ------------------------------
    def _construir_botones_admin(self, parent):
        opciones = [
            ("Gestión de Usuarios", self.abrir_gestion_usuarios),
            ("Gestión de Reservas", self.abrir_gestion_reservas),
            ("Gestión de Recibos", self.abrir_gestion_recibos),
            ("Notificaciones", self.abrir_notificaciones),
        ]

        for texto, comando in opciones:
            ttk.Button(parent, text=texto, command=comando).pack(fill="x", padx=150, pady=10)

    # ------------------------------
    #     VENTANAS SECUNDARIAS
    # ------------------------------
    def abrir_aparatos(self):
        ventana = tk.Toplevel(self.root)
        VentanaAparatos(ventana)

    def abrir_clases(self):
        ventana = tk.Toplevel(self.root)
        VentanaClases(ventana)

    def abrir_rutinas(self):
        ventana = tk.Toplevel(self.root)
        VentanaRutinas(ventana)

    def abrir_pagos(self):
        ventana = tk.Toplevel(self.root)
        VentanaPagos(ventana)

    def abrir_gestion_usuarios(self):
        ventana = tk.Toplevel(self.root)
        VentanaGestionUsuarios(ventana)

    def abrir_gestion_reservas(self):
        ventana = tk.Toplevel(self.root)
        VentanaGestionReservas(ventana)

    def abrir_gestion_recibos(self):
        ventana = tk.Toplevel(self.root)
        VentanaGestionRecibos(ventana)

    def abrir_notificaciones(self):
        ventana = tk.Toplevel(self.root)
        VentanaNotificaciones(ventana)


if __name__ == "__main__":
    root = tk.Tk()
    MenuPrincipal(root, ROL_CLIENTE)
    root.mainloop()
