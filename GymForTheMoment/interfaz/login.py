import tkinter as tk
from tkinter import ttk
from servicios.servicio_clientes import ServicioClientes
from interfaz.menu_principal import MenuPrincipal
from utilidades.ui import set_uniform_window

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym For The Moment - Inicio de Sesión")
        # Ajustar tamaño uniforme y centrado
        set_uniform_window(self.root, width_frac=0.6, height_frac=0.7, min_width=800, min_height=600)

        self.servicio_clientes = ServicioClientes()
        self.servicio_clientes.crear_usuarios_iniciales()

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
        sombra = tk.Frame(self.root, bg="#CCCCCC")
        sombra.place(relx=0.5, rely=0.5, anchor="center", width=450, height=480)

        self.marco = tk.Frame(self.root, bg="#F5F5F5", bd=0)
        self.marco.place(relx=0.5, rely=0.5, anchor="center", width=440, height=470)

        tk.Label(self.marco, text="GYM FOR THE MOMENT", bg="#F5F5F5", fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(pady=(40, 30))

        ttk.Label(self.marco, text="Usuario:", background="#F5F5F5").pack(anchor="w", padx=50, pady=(0, 5))
        self.entry_usuario = ttk.Entry(self.marco)
        self.entry_usuario.pack(fill="x", padx=50, pady=(0, 5))

        ttk.Label(self.marco, text="Contraseña:", background="#F5F5F5").pack(anchor="w", padx=50, pady=(10, 5))
        self.entry_contrasena = ttk.Entry(self.marco, show="*")
        self.entry_contrasena.pack(fill="x", padx=50, pady=(0, 5))

        self.label_error = tk.Label(self.marco, text="", fg="red", bg="#F5F5F5", font=("Segoe UI", 10))
        self.label_error.pack(pady=(5, 10))

        ttk.Button(self.marco, text="Iniciar Sesión", command=self.login_usuario).pack(fill="x", padx=50, pady=(0, 15))
        ttk.Button(self.marco, text="Crear una cuenta", command=self.abrir_registro).pack(fill="x", padx=50)

        tk.Label(self.marco, text="© 2025 Gym For The Moment", bg="#F5F5F5", fg="#555555", font=("Segoe UI", 10)).pack(side="bottom", pady=15)

    def login_usuario(self):
        self.label_error.config(text="")
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not usuario or not contrasena:
            self.label_error.config(text="Debe completar todos los campos")
            return

        if len(usuario) < 1 or len(contrasena) < 1:
            self.label_error.config(text="Usuario o contraseña vacíos")
            return

        usuario_db = self.servicio_clientes.obtener_cliente_por_usuario(usuario)

        if usuario_db and contrasena == usuario_db.contrasena:
            rol = usuario_db.rol
        else:
            self.label_error.config(text="Usuario o contraseña incorrectos")
            # Limpiar campo de contraseña por seguridad
            self.entry_contrasena.delete(0, tk.END)
            return

        self.root.destroy()
        root_menu = tk.Tk()
        MenuPrincipal(root_menu, rol, usuario_db.usuario)
        root_menu.mainloop()

    def abrir_registro(self):
        from interfaz.registro import Registro
        self.root.withdraw()
        registro_ventana = tk.Toplevel()
        Registro(registro_ventana, self.root)

