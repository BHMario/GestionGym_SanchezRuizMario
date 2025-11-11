import tkinter as tk
from tkinter import messagebox
from servicios.servicio_reservas import ServicioReservas

class VentanaNotificaciones:
    def __init__(self, root):
        self.root = root
        self.root.title("Notificaciones")
        self.root.geometry("600x400")
        self.servicio_reservas = ServicioReservas()

        tk.Label(root, text="Notificaciones de Solicitudes de Clientes", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(root, width=70)
        self.listbox.pack(pady=10)

        tk.Button(root, text="Actualizar", command=self.cargar_notificaciones).pack(pady=5)

        self.cargar_notificaciones()

    def cargar_notificaciones(self):
        self.listbox.delete(0, tk.END)
        solicitudes = self.servicio_reservas.listar_solicitudes_pendientes()
        for s in solicitudes:
            self.listbox.insert(tk.END, f"{s.id} - {s.cliente} - {s.aparato} - {s.hora} - {s.estado}")
