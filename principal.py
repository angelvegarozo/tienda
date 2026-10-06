import tkinter as tk
from tkinter import ttk
from inicio_sesion import VentanaLogin, NEGRO, GRIS, BLANCO, MORADO, MORADO_CLARO
from registro_usuario import VentanaRegistro


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tienda - Autenticación")
        self.configure(bg=NEGRO)
        self.resizable(False, False)
        self.clientes = []      # aquí guardamos los clientes mientras el programa está abierto
        self._pantalla = None
        self.aplicar_estilo()
        self.mostrar_login()

    def aplicar_estilo(self):
        # el Combobox es de ttk, por eso se pinta aparte con un estilo
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TCombobox", fieldbackground=GRIS, background=MORADO,
                         foreground=BLANCO, arrowcolor=BLANCO, bordercolor=GRIS,
                         lightcolor=GRIS, darkcolor=GRIS)
        estilo.map("TCombobox",
                   fieldbackground=[("readonly", GRIS)],
                   foreground=[("readonly", BLANCO)],
                   selectbackground=[("readonly", GRIS)],
                   selectforeground=[("readonly", BLANCO)])
        # colores de la lista que se despliega
        self.option_add("*TCombobox*Listbox.background", GRIS)
        self.option_add("*TCombobox*Listbox.foreground", BLANCO)
        self.option_add("*TCombobox*Listbox.selectBackground", MORADO)
        self.option_add("*TCombobox*Listbox.selectForeground", BLANCO)

    def mostrar(self, clase_ventana):
        # sirve para cualquier pantalla que herede de VentanaBase
        if self._pantalla is not None:
            self._pantalla.destroy()
        self._pantalla = clase_ventana(self)
        self._pantalla.pack(padx=20, pady=20)

    def mostrar_login(self):
        self.mostrar(VentanaLogin)

    def mostrar_registro(self):
        self.mostrar(VentanaRegistro)


if __name__ == "__main__":
    App().mainloop()