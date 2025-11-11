import tkinter as tk
from tkinter import messagebox
from servicios.servicio_reservas import ServicioReservas

class VentanaClases:
    def __init__(self, root):
        self.root = root
        self.root.title("Clases/Sesiones - Gym For The Moment")
        self.root.geometry("500x400")
        self.servicio_reservas = ServicioReservas()

        tk.Label(root, text="Listado de Clases/Sesiones", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10)

        self.boton_solicitar = tk.Button(root, text="Solicitar Reserva", command=self.solicitar_reserva)
        self.boton_solicitar.pack(pady=5)

        self.cargar_clases()

    def cargar_clases(self):
        self.listbox.delete(0, tk.END)
        sesiones = self.servicio_reservas.listar_sesiones()
        for sesion in sesiones:
            estado = "Ocupado" if sesion.ocupado else "Libre"
            self.listbox.insert(tk.END, f"{sesion.id} - {sesion.nombre} - {estado}")

    def solicitar_reserva(self):
        seleccionado = self.listbox.curselection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Debe seleccionar una sesión")
            return
        # Solicitud de reserva al administrador
        messagebox.showinfo("Solicitud enviada", "Su solicitud de reserva ha sido enviada al administrador")
