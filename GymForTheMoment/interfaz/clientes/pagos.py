import tkinter as tk
from tkinter import ttk
from servicios.servicio_clientes import ServicioClientes
from utilidades.ui import set_uniform_window

class VentanaPagos:
    def __init__(self, root, cliente_actual=None, callback_refrescar=None):
        self.root = root
        self.cliente_actual = cliente_actual or "usuario1"
        self.servicio_clientes = ServicioClientes()
        self.callback_refrescar = callback_refrescar

        self.root.title("Pasarela de Pagos - Gym For The Moment")
        # Ampliar ligeramente la ventana para asegurar que los mensajes se ven completos
        set_uniform_window(self.root, width_frac=0.6, height_frac=0.8, min_width=900, min_height=700)
        self.root.configure(bg="#FFFFFF")

        self.metodo_pago = tk.StringVar(value="Tarjeta")
        self.campos_pago = []

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

        # Contenedor principal (expandible) y zona de mensajes fija al fondo
        content_frame = tk.Frame(self.root, bg="#FFFFFF")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(10, 0))

        card = ttk.Frame(content_frame, style="Card.TFrame")
        card.pack(pady=10, padx=40, fill="both", expand=False)
        card_inner = tk.Frame(card, bg="#F0F7FF")
        card_inner.pack(padx=20, pady=20, fill="both")

        tk.Label(card_inner, text="Monto a Pagar:", bg="#F0F7FF",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(card_inner, text="50 € / Mensualidad", bg="#F0F7FF",
                 font=("Segoe UI", 16)).pack(anchor="w", pady=(0, 10))

        tk.Label(card_inner, text="Seleccione Método de Pago:", bg="#F0F7FF",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(10, 5))

        for metodo in ["Tarjeta", "PayPal", "Bizum"]:
            ttk.Radiobutton(card_inner, text=metodo, value=metodo, variable=self.metodo_pago,
                            style="Metodo.TRadiobutton",
                            command=self._actualizar_campos_pago).pack(anchor="w", padx=10)

        self.frame_campos = tk.Frame(content_frame, bg="#FFFFFF")
        self.frame_campos.pack(pady=20)
        self._actualizar_campos_pago()

        pagar_btn = tk.Button(content_frame, text="Pagar Ahora", bg="#2196F3", fg="white",
                  font=("Segoe UI", 14, "bold"), command=self.simular_pago, bd=0, relief="flat")
        pagar_btn.pack(pady=10, ipadx=20, ipady=8)
        pagar_btn.bind("<Enter>", lambda e: pagar_btn.config(bg="#1976D2"))
        pagar_btn.bind("<Leave>", lambda e: pagar_btn.config(bg="#2196F3"))

        # Zona de mensajes fija en la parte inferior para que siempre sea visible
        self.label_mensaje = tk.Label(self.root, text="", bg="#FFFFFF", fg="red", font=("Segoe UI", 12, "bold"))
        self.label_mensaje.pack(side="bottom", fill="x", pady=8)

    def _actualizar_campos_pago(self):
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        self.campos_pago = []

        metodo = self.metodo_pago.get()
        if metodo == "Tarjeta":
            for texto, ancho in [("Número de Tarjeta", 25), ("Fecha de Vencimiento (MM/AA)", 10), ("CVV", 5)]:
                tk.Label(self.frame_campos, text=texto, bg="#FFFFFF").pack(anchor="w")
                e = tk.Entry(self.frame_campos, width=ancho, show="*" if texto == "CVV" else "")
                e.pack(pady=5)
                self.campos_pago.append(e)
        elif metodo == "PayPal":
            tk.Label(self.frame_campos, text="Correo de PayPal", bg="#FFFFFF").pack(anchor="w")
            e = tk.Entry(self.frame_campos, width=30)
            e.pack(pady=5)
            self.campos_pago.append(e)
        elif metodo == "Bizum":
            tk.Label(self.frame_campos, text="Número de Teléfono", bg="#FFFFFF").pack(anchor="w")
            e = tk.Entry(self.frame_campos, width=20)
            e.pack(pady=5)
            self.campos_pago.append(e)

    def simular_pago(self):
        for campo in self.campos_pago:
            if not campo.get().strip():
                self.label_mensaje.config(text="Por favor, complete todos los datos antes de pagar", fg="red")
                return

        metodo = self.metodo_pago.get()
        
        # Validaciones adicionales según el método
        try:
            if metodo == "Tarjeta":
                num_tarjeta = self.campos_pago[0].get().strip()
                fecha_venc = self.campos_pago[1].get().strip()
                cvv = self.campos_pago[2].get().strip()
                
                # Validar número de tarjeta (solo dígitos, 13-19 dígitos)
                if not num_tarjeta.isdigit() or len(num_tarjeta) < 13 or len(num_tarjeta) > 19:
                    self.label_mensaje.config(text="Número de tarjeta inválido (13-19 dígitos)", fg="red")
                    return
                
                # Validar fecha (MM/AA)
                if "/" not in fecha_venc or len(fecha_venc.split("/")) != 2:
                    self.label_mensaje.config(text="Fecha de vencimiento inválida (formato: MM/AA)", fg="red")
                    return
                mes, año = fecha_venc.split("/")
                if not mes.isdigit() or not año.isdigit() or int(mes) < 1 or int(mes) > 12:
                    self.label_mensaje.config(text="Mes inválido en fecha de vencimiento", fg="red")
                    return
                
                # Validar CVV (3-4 dígitos)
                if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
                    self.label_mensaje.config(text="CVV inválido (3-4 dígitos)", fg="red")
                    return
                    
            elif metodo == "PayPal":
                email = self.campos_pago[0].get().strip()
                # Validar email básico
                if "@" not in email or "." not in email.split("@")[-1]:
                    self.label_mensaje.config(text="Email de PayPal inválido", fg="red")
                    return
                    
            elif metodo == "Bizum":
                telefono = self.campos_pago[0].get().strip()
                # Validar teléfono (solo dígitos, al menos 9)
                if not telefono.isdigit() or len(telefono) < 9:
                    self.label_mensaje.config(text="Número de teléfono inválido (al menos 9 dígitos)", fg="red")
                    return
        except Exception as e:
            self.label_mensaje.config(text=f"Error en validación: {str(e)}", fg="red")
            return

        # Procesar el pago
        try:
            self.servicio_clientes.marcar_pagado(self.cliente_actual)
            self.label_mensaje.config(
                text=f"✓ Pago mediante {metodo} completado correctamente. ¡Gracias, {self.cliente_actual}!", 
                fg="green"
            )

            if self.callback_refrescar:
                try:
                    self.callback_refrescar()
                except Exception:
                    pass

            for campo in self.campos_pago:
                campo.delete(0, tk.END)
        except Exception as e:
            self.label_mensaje.config(text=f"Error al procesar el pago: {str(e)}", fg="red")

