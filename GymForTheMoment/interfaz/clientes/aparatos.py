import tkinter as tk
from tkinter import messagebox
from servicios.servicio_aparatos import ServicioAparatos

class VentanaAparatos:
    def __init__(self, root):
        self.root = root
        self.root.title("Aparatos - Gym For The Moment")
        self.root.geometry("500x400")
        self.servicio_aparatos = ServicioAparatos()

        tk.Label(root, text="Listado de Aparatos", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10)

        self.boton_solicitar = tk.Button(root, text="Solicitar Reserva", command=self.solicitar_reserva)
        self.boton_solicitar.pack(pady=5)

        self.cargar_aparatos()

    def cargar_aparatos(self):
        self.listbox.delete(0, tk.END)
        aparatos = self.servicio_aparatos.listar_aparatos()
        for aparato in aparatos:
            self.listbox.insert(tk.END, f"{aparato.id} - {aparato.nombre} - {'Ocupado' if aparato.ocupado else 'Libre'}")

    def solicitar_reserva(self):
        seleccionado = self.listbox.curselection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Debe seleccionar un aparato")
            return
        # Aquí se enviaría la solicitud de reserva al administrador
        messagebox.showinfo("Solicitud enviada", "Su solicitud de reserva ha sido enviada al administrador")
