import tkinter as tk
from tkinter import messagebox

# Importar submenús
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
        self.root.title("Gym For The Moment - Menú Principal")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        tk.Label(root, text=f"Bienvenido ({rol})", font=("Arial", 14)).pack(pady=20)

        # Crear botones según rol
        if rol == ROL_CLIENTE:
            self.boton_clientes()
        elif rol == ROL_ADMINISTRADOR:
            self.boton_administradores()
        else:
            messagebox.showerror("Error", "Rol desconocido")
            root.destroy()

    # --- Botones clientes ---
    def boton_clientes(self):
        tk.Button(self.root, text="Ver Aparatos", width=25, command=self.abrir_aparatos).pack(pady=5)
        tk.Button(self.root, text="Ver Clases/Sesiones", width=25, command=self.abrir_clases).pack(pady=5)
        tk.Button(self.root, text="Ver Rutinas", width=25, command=self.abrir_rutinas).pack(pady=5)
        tk.Button(self.root, text="Pasarela de Pagos", width=25, command=self.abrir_pagos).pack(pady=5)

    # --- Botones administradores ---
    def boton_administradores(self):
        tk.Button(self.root, text="Gestión de Usuarios", width=25, command=self.abrir_gestion_usuarios).pack(pady=5)
        tk.Button(self.root, text="Gestión de Reservas", width=25, command=self.abrir_gestion_reservas).pack(pady=5)
        tk.Button(self.root, text="Gestión de Recibos", width=25, command=self.abrir_gestion_recibos).pack(pady=5)
        tk.Button(self.root, text="Notificaciones", width=25, command=self.abrir_notificaciones).pack(pady=5)

    # --- Funciones para abrir submenús ---
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


# Para probar el menú de manera independiente
if __name__ == "__main__":
    root = tk.Tk()
    MenuPrincipal(root, ROL_CLIENTE)  # O ROL_ADMINISTRADOR
    root.mainloop()
