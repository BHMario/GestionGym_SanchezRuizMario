import tkinter as tk

def set_uniform_window(root, width_frac=0.9, height_frac=0.85, min_width=900, min_height=650):
    # Ajustar la ventana `root` a un tamaño uniforme y centrado según el tamaño de pantalla.
    try:
        root.update_idletasks()
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        w = max(int(sw * width_frac), min_width)
        h = max(int(sh * height_frac), min_height)
        x = max((sw - w) // 2, 0)
        y = max((sh - h) // 2, 0)
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.minsize(min_width, min_height)
        # Permitir redimensionar verticalmente y horizontal si hace falta.
        root.resizable(True, True)
    except Exception:
        pass

