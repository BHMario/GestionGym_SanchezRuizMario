import tkinter as tk
from tkinter import messagebox
from servicios.servicio_clientes import ServicioClientes
from utilidades.validadores import validar_email

class Registro:
    def __init__(self, root, login_root):
        """
        root: ventana de registro
        login_root: ventana login que la llamó, para mostrarla de nuevo después
        """
        self.root = root
        self.login_root = login_root
        self.root.title("Registro de Cliente")
        self.root.geometry("350x250")
        self.root.resizable(False, False)

        self.servicio_clientes = ServicioClientes()

        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack(pady=5)

        tk.Label(root, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(root)
        self.entry_email.pack(pady=5)

        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_contrasena = tk.Entry(root, show="*")
        self.entry_contrasena.pack(pady=5)

        tk.Button(root, text="Registrarse", width=20, command=self.registrar_usuario).pack(pady=10)
        tk.Button(root, text="Cancelar", width=20, command=self.cancelar_registro).pack(pady=5)

    def registrar_usuario(self):
        usuario = self.entry_usuario.get()
        email = self.entry_email.get()
        contrasena = self.entry_contrasena.get()

        if not usuario or not email or not contrasena:
            messagebox.showerror("Error", "Debe completar todos los campos")
            return
        if not validar_email(email):
            messagebox.showerror("Error", "Email inválido")
            return

        if self.servicio_clientes.obtener_cliente_por_usuario(usuario):
            messagebox.showerror("Error", "El usuario ya existe")
            return

        self.servicio_clientes.agregar_cliente(usuario=usuario, email=email, contrasena=contrasena)
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        self.root.destroy()
        self.login_root.deiconify()  # Mostrar de nuevo la ventana de login

    def cancelar_registro(self):
        self.root.destroy()
        self.login_root.deiconify()
