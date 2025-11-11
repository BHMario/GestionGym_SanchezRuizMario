import tkinter as tk
from tkinter import messagebox
from servicios.servicio_clientes import ServicioClientes

class VentanaGestionUsuarios:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Usuarios")
        self.root.geometry("600x400")
        self.servicio_clientes = ServicioClientes()

        tk.Label(root, text="Listado de Clientes", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(root, width=70)
        self.listbox.pack(pady=10)

        tk.Button(root, text="Actualizar Estado de Pago", command=self.actualizar_pago).pack(pady=5)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.listbox.delete(0, tk.END)
        clientes = self.servicio_clientes.listar_clientes()
        for c in clientes:
            estado_pago = "Pagado" if c.pagado else "Moroso"
            self.listbox.insert(tk.END, f"{c.id} - {c.usuario} - {c.email} - {estado_pago}")

    def actualizar_pago(self):
        seleccionado = self.listbox.curselection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Debe seleccionar un usuario")
            return
        # Ejemplo: alternar estado de pago
        indice = seleccionado[0]
        clientes = self.servicio_clientes.listar_clientes()
        cliente = clientes[indice]
        cliente.pagado = not cliente.pagado
        self.cargar_usuarios()
        messagebox.showinfo("Éxito", f"Estado de pago actualizado para {cliente.usuario}")
