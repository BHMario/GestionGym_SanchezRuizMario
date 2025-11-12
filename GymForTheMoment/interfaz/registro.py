import tkinter as tk
from tkinter import ttk
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
        self.root.geometry("1100x750")  # Ventana más grande
        self.root.resizable(False, False)
        self.root.configure(bg="#FFFFFF")  # Fondo blanco

        self.servicio_clientes = ServicioClientes()

        self._configurar_estilos()
        self._construir_interfaz()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#F5F5F5", foreground="#222222", font=("Segoe UI", 12))
        style.configure("TEntry", padding=10, font=("Segoe UI", 12))
        style.configure("TButton",
                        background="#333333",
                        foreground="white",
                        font=("Segoe UI", 12, "bold"),
                        padding=10)
        style.map("TButton",
                  background=[("active", "#555555")],
                  foreground=[("active", "white")])

    def _construir_interfaz(self):
        # Sombra de la tarjeta
        sombra = tk.Frame(self.root, bg="#CCCCCC")
        sombra.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)

        # Tarjeta central
        self.marco = tk.Frame(self.root, bg="#F5F5F5", bd=0)
        self.marco.place(relx=0.5, rely=0.5, anchor="center", width=490, height=590)

        # Título elegante
        tk.Label(self.marco, text="REGISTRO DE CLIENTE", bg="#F5F5F5", fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(pady=(40, 30))

        # Usuario
        ttk.Label(self.marco, text="Usuario:", background="#F5F5F5").pack(anchor="w", padx=50, pady=(0, 5))
        self.entry_usuario = ttk.Entry(self.marco)
        self.entry_usuario.pack(fill="x", padx=50, pady=(0, 5))

        # Email
        ttk.Label(self.marco, text="Email:", background="#F5F5F5").pack(anchor="w", padx=50, pady=(10, 5))
        self.entry_email = ttk.Entry(self.marco)
        self.entry_email.pack(fill="x", padx=50, pady=(0, 5))

        # Contraseña
        ttk.Label(self.marco, text="Contraseña:", background="#F5F5F5").pack(anchor="w", padx=50, pady=(10, 5))
        self.entry_contrasena = ttk.Entry(self.marco, show="*")
        self.entry_contrasena.pack(fill="x", padx=50, pady=(0, 15))

        # Label de error (vacío inicialmente)
        self.label_error = tk.Label(self.marco, text="", fg="red", bg="#F5F5F5", font=("Segoe UI", 10))
        self.label_error.pack(pady=(5, 10))

        # Botones
        ttk.Button(self.marco, text="Registrarse", command=self.registrar_usuario).pack(fill="x", padx=50, pady=(0, 10))
        ttk.Button(self.marco, text="Cancelar", command=self.cancelar_registro).pack(fill="x", padx=50)

        # Pie de la tarjeta
        tk.Label(self.marco, text="© 2025 Gym For The Moment", bg="#F5F5F5", fg="#555555", font=("Segoe UI", 10)).pack(side="bottom", pady=15)

    def registrar_usuario(self):
        self.label_error.config(text="")  # Limpiar mensaje previo
        usuario = self.entry_usuario.get().strip()
        email = self.entry_email.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not usuario or not email or not contrasena:
            self.label_error.config(text="Debe completar todos los campos")
            return
        if not validar_email(email):
            self.label_error.config(text="Email inválido")
            return

        if self.servicio_clientes.obtener_cliente_por_usuario(usuario):
            self.label_error.config(text="El usuario ya existe")
            return

        self.servicio_clientes.agregar_cliente(usuario=usuario, email=email, contrasena=contrasena)
        self.label_error.config(fg="green", text="Usuario registrado correctamente")
        self.root.after(1500, self._cerrar_y_volver_login)

    def _cerrar_y_volver_login(self):
        self.root.destroy()
        self.login_root.deiconify()

    def cancelar_registro(self):
        self.root.destroy()
        self.login_root.deiconify()
