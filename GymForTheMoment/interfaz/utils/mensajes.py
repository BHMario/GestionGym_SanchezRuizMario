import tkinter.messagebox as messagebox

class Mensajes:
    @staticmethod
    def error(titulo: str, mensaje: str):
        messagebox.showerror(titulo, mensaje)

    @staticmethod
    def info(titulo: str, mensaje: str):
        messagebox.showinfo(titulo, mensaje)

    @staticmethod
    def aviso(titulo: str, mensaje: str):
        messagebox.showwarning(titulo, mensaje)
