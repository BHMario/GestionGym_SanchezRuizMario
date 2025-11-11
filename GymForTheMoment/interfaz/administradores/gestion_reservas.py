import tkinter as tk
from tkinter import messagebox
from servicios.servicio_reservas import ServicioReservas

class VentanaGestionReservas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Reservas")
        self.root.geometry("600x400")
        self.servicio_reservas = ServicioReservas()

        tk.Label(root, text="Listado de Reservas", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(root, width=70)
        self.listbox.pack(pady=10)

        tk.Button(root, text="Aceptar Reserva", command=self.aceptar_reserva).pack(pady=5)
        tk.Button(root, text="Denegar Reserva", command=self.denegar_reserva).pack(pady=5)

        self.cargar_reservas()

    def cargar_reservas(self):
        self.listbox.delete(0, tk.END)
        reservas = self.servicio_reservas.listar_reservas_pendientes()
        for r in reservas:
            self.listbox.insert(tk.END, f"{r.id} - {r.cliente} - {r.aparato} - {r.hora} - {r.estado}")

    def aceptar_reserva(self):
        seleccionado = self.listbox.curselection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Debe seleccionar una reserva")
            return
        indice = seleccionado[0]
        reservas = self.servicio_reservas.listar_reservas_pendientes()
        reserva = reservas[indice]
        self.servicio_reservas.aceptar_reserva(reserva)
        self.cargar_reservas()
        messagebox.showinfo("Éxito", "Reserva aceptada")

    def denegar_reserva(self):
        seleccionado = self.listbox.curselection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Debe seleccionar una reserva")
            return
        indice = seleccionado[0]
        reservas = self.servicio_reservas.listar_reservas_pendientes()
        reserva = reservas[indice]
        self.servicio_reservas.denegar_reserva(reserva)
        self.cargar_reservas()
        messagebox.showinfo("Éxito", "Reserva denegada")
