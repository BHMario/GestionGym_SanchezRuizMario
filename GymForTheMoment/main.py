import tkinter as tk
from interfaz.login import Login


def main():
    root = tk.Tk()
    app = Login(root)
    root.mainloop()


if __name__ == "__main__":
    main()

