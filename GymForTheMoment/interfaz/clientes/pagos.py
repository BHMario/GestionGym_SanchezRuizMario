import tkinter as tk
from tkinter import ttk

class VentanaPagos:
    def __init__(self, root):
        self.root = root
        self.root.title("Pasarela de Pagos - Gym For The Moment")
        self.root.geometry("800x700")
        self.root.configure(bg="#FFFFFF")

        self.metodo_pago = tk.StringVar(value="Tarjeta")
        self.campos_pago = []  # Para guardar referencias a los Entry dinámicos

        self._configurar_estilos()
        self._construir_interfaz()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#FFFFFF", foreground="#222222", font=("Segoe UI", 12))
        style.configure("TButton", font=("Segoe UI", 13, "bold"))
        style.configure("Card.TFrame", background="#F5F5F5", relief="ridge", borderwidth=2)
        style.configure("Metodo.TRadiobutton", background="#FFFFFF", font=("Segoe UI", 12))

    def _construir_interfaz(self):
        tk.Label(self.root, text="GYM FOR THE MOMENT", bg="#FFFFFF", fg="#222222",
                 font=("Segoe UI", 24, "bold")).pack(pady=20)

        card = ttk.Frame(self.root, style="Card.TFrame")
        card.pack(pady=10, padx=40, fill="both", expand=False)
        card_inner = tk.Frame(card, bg="#F5F5F5")
        card_inner.pack(padx=20, pady=20)

        tk.Label(card_inner, text="Monto a Pagar:", bg="#F5F5F5",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(card_inner, text="50 € / Mensualidad", bg="#F5F5F5",
                 font=("Segoe UI", 16)).pack(anchor="w", pady=(0, 10))

        tk.Label(card_inner, text="Seleccione Método de Pago:", bg="#F5F5F5",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(10, 5))

        metodos = ["Tarjeta", "PayPal", "Bizum"]
        for metodo in metodos:
            ttk.Radiobutton(card_inner, text=metodo, value=metodo, variable=self.metodo_pago,
                            style="Metodo.TRadiobutton",
                            command=self._actualizar_campos_pago).pack(anchor="w", padx=10)

        self.frame_campos = tk.Frame(self.root, bg="#FFFFFF")
        self.frame_campos.pack(pady=20)
        self._actualizar_campos_pago()

        boton_pagar = tk.Button(self.root, text="Pagar Ahora", bg="#333333", fg="white",
                                font=("Segoe UI", 14, "bold"), command=self.simular_pago)
        boton_pagar.pack(pady=10, ipadx=20, ipady=8)

        self.label_mensaje = tk.Label(self.root, text="", bg="#FFFFFF", fg="red", font=("Segoe UI", 12, "bold"))
        self.label_mensaje.pack(pady=10)

    def _actualizar_campos_pago(self):
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        self.campos_pago = []

        metodo = self.metodo_pago.get()

        if metodo == "Tarjeta":
            tk.Label(self.frame_campos, text="Número de Tarjeta", bg="#FFFFFF").pack(anchor="w")
            numero = tk.Entry(self.frame_campos, width=25)
            numero.pack(pady=5)
            self.campos_pago.append(numero)

            tk.Label(self.frame_campos, text="Fecha de Vencimiento (MM/AA)", bg="#FFFFFF").pack(anchor="w")
            vencimiento = tk.Entry(self.frame_campos, width=10)
            vencimiento.pack(pady=5)
            self.campos_pago.append(vencimiento)

            tk.Label(self.frame_campos, text="CVV", bg="#FFFFFF").pack(anchor="w")
            cvv = tk.Entry(self.frame_campos, width=5, show="*")
            cvv.pack(pady=5)
            self.campos_pago.append(cvv)

        elif metodo == "PayPal":
            tk.Label(self.frame_campos, text="Correo de PayPal", bg="#FFFFFF").pack(anchor="w")
            correo = tk.Entry(self.frame_campos, width=30)
            correo.pack(pady=5)
            self.campos_pago.append(correo)

        elif metodo == "Bizum":
            tk.Label(self.frame_campos, text="Número de Teléfono", bg="#FFFFFF").pack(anchor="w")
            telefono = tk.Entry(self.frame_campos, width=20)
            telefono.pack(pady=5)
            self.campos_pago.append(telefono)

    def simular_pago(self):
        # Validar que todos los campos estén completos
        for campo in self.campos_pago:
            if not campo.get().strip():
                self.label_mensaje.config(text="Por favor, complete todos los datos antes de pagar", fg="red")
                return

        metodo = self.metodo_pago.get()
        self.label_mensaje.config(
            text=f"Pago mediante {metodo} completado correctamente. ¡Gracias por tu compra!",
            fg="green"
        )

        # Limpiar todos los campos después del pago
        for campo in self.campos_pago:
            campo.delete(0, tk.END)
