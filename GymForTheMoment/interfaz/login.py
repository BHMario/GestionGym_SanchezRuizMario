import tkinter as tk
from tkinter import messagebox
from servicios.servicio_clientes import ServicioClientes
from interfaz.menu_principal import MenuPrincipal
from utilidades.constantes import ROL_CLIENTE, ROL_ADMINISTRADOR
from interfaz.registro import Registro

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym For The Moment - Login")
        self.root.geometry("350x200")
        self.root.resizable(False, False)

        # Servicio clientes
        self.servicio_clientes = ServicioClientes()

        # Widgets login
        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack(pady=5)

        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_contrasena = tk.Entry(root, show="*")
        self.entry_contrasena.pack(pady=5)

        tk.Button(root, text="Ingresar", width=20, command=self.login_usuario).pack(pady=10)
        tk.Button(root, text="Registrarse", width=20, command=self.abrir_registro).pack(pady=5)

    def login_usuario(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if not usuario or not contrasena:
            messagebox.showerror("Error", "Debe completar todos los campos")
            return

        # Verificación de login
        cliente = self.servicio_clientes.obtener_cliente_por_usuario(usuario)

        if cliente and contrasena == cliente.contrasena:
            rol = ROL_CLIENTE
        elif usuario == "admin" and contrasena == "admin123":
            rol = ROL_ADMINISTRADOR
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            return

        messagebox.showinfo("Éxito", f"Bienvenido {usuario} ({rol})")
        self.root.destroy()
        root_menu = tk.Tk()
        MenuPrincipal(root_menu, rol)
        root_menu.mainloop()

    def abrir_registro(self):
        self.root.withdraw()  # Oculta la ventana login
        registro_ventana = tk.Toplevel()
        Registro(registro_ventana, self.root)  # Pasamos root para poder mostrar login de nuevo

# Para probar
if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()
