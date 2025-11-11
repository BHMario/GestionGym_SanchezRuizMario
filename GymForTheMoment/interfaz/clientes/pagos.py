import tkinter as tk
from tkinter import messagebox

class VentanaPagos:
    def __init__(self, root):
        self.root = root
        self.root.title("Pasarela de Pagos - Gym For The Moment")
        self.root.geometry("400x300")

        tk.Label(root, text="Pasarela de Pagos (Visual)", font=("Arial", 14)).pack(pady=20)

        tk.Label(root, text="Monto Mensual: $50").pack(pady=5)
        tk.Label(root, text="Método de Pago: Tarjeta de Crédito").pack(pady=5)

        tk.Button(root, text="Pagar (Simulado)", command=self.simular_pago).pack(pady=20)

    def simular_pago(self):
        messagebox.showinfo("Pago", "Pago simulado correctamente")
