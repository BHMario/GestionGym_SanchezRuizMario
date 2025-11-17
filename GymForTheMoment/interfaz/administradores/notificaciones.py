import tkinter as tk
from servicios.servicio_reservas import ServicioReservas
from servicios.servicio_clases import ServicioClases
from servicios.servicio_aparatos import ServicioAparatos

class VentanaNotificaciones:
    def __init__(self, root):
        self.root = root
        self.root.title("Notificaciones")
        self.root.geometry("600x450")
        self.servicio_reservas = ServicioReservas()
        self.servicio_clases = ServicioClases()
        self.servicio_aparatos = ServicioAparatos()

        tk.Label(root, text="Notificaciones de Solicitudes de Clientes", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(root, width=70)
        self.listbox.pack(pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar_solicitud)

        # Botones aceptar/rechazar
        self.frame_botones = tk.Frame(root)
        self.frame_botones.pack(pady=10)

        self.btn_aceptar = tk.Button(
            self.frame_botones, text="Aceptar", bg="#4CAF50", fg="white",
            font=("Arial", 12, "bold"), command=self.aceptar_reserva, state="disabled"
        )
        self.btn_aceptar.pack(side="left", padx=10)

        self.btn_rechazar = tk.Button(
            self.frame_botones, text="Rechazar", bg="#F44336", fg="white",
            font=("Arial", 12, "bold"), command=self.rechazar_reserva, state="disabled"
        )
        self.btn_rechazar.pack(side="left", padx=10)

        # Variable para almacenar la reserva seleccionada
        self.reserva_seleccionada = None

        # Actualizar la lista automáticamente
        self.cargar_notificaciones()
        self.root.after(5000, self.actualizar_periodicamente)

    def cargar_notificaciones(self):
        self.listbox.delete(0, tk.END)
        solicitudes = self.servicio_reservas.listar_solicitudes_pendientes()
        for s in solicitudes:
            self.listbox.insert(tk.END, f"{s.id} - {s.cliente} - {s.aparato} - {s.hora} - {s.estado}")
        # Desactivar botones si no hay selección
        self.btn_aceptar.config(state="disabled")
        self.btn_rechazar.config(state="disabled")
        self.reserva_seleccionada = None

    def actualizar_periodicamente(self):
        self.cargar_notificaciones()
        self.root.after(5000, self.actualizar_periodicamente)

    def seleccionar_solicitud(self, event):
        try:
            index = self.listbox.curselection()[0]
            texto = self.listbox.get(index)
            # Extraer el ID de la reserva desde el texto
            reserva_id = int(texto.split(" - ")[0])
            reservas = self.servicio_reservas.listar_solicitudes_pendientes()
            self.reserva_seleccionada = next((r for r in reservas if r.id == reserva_id), None)
            if self.reserva_seleccionada:
                self.btn_aceptar.config(state="normal")
                self.btn_rechazar.config(state="normal")
        except IndexError:
            self.reserva_seleccionada = None
            self.btn_aceptar.config(state="disabled")
            self.btn_rechazar.config(state="disabled")

    def aceptar_reserva(self):
        if self.reserva_seleccionada:
            self.servicio_reservas.aceptar_reserva(self.reserva_seleccionada)
            nombre = self.reserva_seleccionada.aparato.lower()

            # Determinar si es aparato o clase
            aparatos = [a.nombre.lower() for a in self.servicio_aparatos.listar_aparatos()]
            clases = [c.nombre.lower() for c in self.servicio_clases.listar_clases()]

            if nombre in aparatos:
                # Marcar aparato ocupado 30 min
                self.servicio_aparatos.marcar_ocupado(nombre, minutos=30)
            elif nombre in clases:
                # Marcar clase ocupada 30 min
                self.servicio_clases.marcar_ocupado(nombre, minutos=30)

            self.cargar_notificaciones()

    def rechazar_reserva(self):
        if self.reserva_seleccionada:
            self.servicio_reservas.denegar_reserva(self.reserva_seleccionada)
            self.cargar_notificaciones()
