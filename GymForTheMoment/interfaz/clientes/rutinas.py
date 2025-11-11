import tkinter as tk
from tkinter import messagebox

class VentanaRutinas:
    def __init__(self, root):
        self.root = root
        self.root.title("Rutinas - Gym For The Moment")
        self.root.geometry("500x400")

        tk.Label(root, text="Seleccione su Rutina", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10)

        # Ejemplo de rutinas (en un futuro se cargarían desde BD)
        rutinas = ["Rutina Full Body", "Rutina Cardio", "Rutina Fuerza", "Rutina Yoga"]
        for rutina in rutinas:
            self.listbox.insert(tk.END, rutina)

        tk.Button(root, text="Seleccionar Rutina", command=self.seleccionar_rutina).pack(pady=5)

    def seleccionar_rutina(self):
        seleccionado = self.listbox.curselection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Debe seleccionar una rutina")
            return
        rutina = self.listbox.get(seleccionado)
        messagebox.showinfo("Rutina seleccionada", f"Ha seleccionado: {rutina}")
