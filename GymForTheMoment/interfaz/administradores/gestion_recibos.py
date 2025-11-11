import tkinter as tk
from tkinter import messagebox
from servicios.servicio_recibos import ServicioRecibos

class VentanaGestionRecibos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Recibos")
        self.root.geometry("600x400")
        self.servicio_recibos = ServicioRecibos()

        tk.Label(root, text="Generación y Control de Recibos", font=("Arial", 14)).pack(pady=10)

        tk.Button(root, text="Generar Recibos Mensuales", command=self.generar_recibos).pack(pady=10)
        tk.Button(root, text="Ver Clientes Morosos", command=self.ver_morosos).pack(pady=5)

    def generar_recibos(self):
        self.servicio_recibos.generar_recibos_mes()
        messagebox.showinfo("Éxito", "Recibos generados correctamente")

    def ver_morosos(self):
        morosos = self.servicio_recibos.listar_morosos()
        mensaje = "\n".join([f"{c.usuario} - {c.email}" for c in morosos])
        if not mensaje:
            mensaje = "No hay clientes morosos"
        messagebox.showinfo("Clientes Morosos", mensaje)
