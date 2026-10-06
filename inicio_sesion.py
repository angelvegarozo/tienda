import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

# los colores quedan aquí arriba para cambiarlos fácil
MORADO = "#7C3AED"
MORADO_CLARO = "#A78BFA"
LILA = "#DDD6FE"
NEGRO = "#0D0D12"
GRIS = "#1C1C26"
BLANCO = "#FFFFFF"
VERDE = "#4ADE80"
ROJO = "#F87171"
FUENTE = "Arial"


class VentanaBase(tk.Frame, ABC):
    # el molde de todas las pantallas: obliga a que cada una tenga estos 3 métodos
    # y además trae los widgets ya decorados para no repetir código

    def __init__(self, app):
        super().__init__(app, bg=NEGRO)
        self.app = app
        self.construir_widgets()
        self._lbl_mensaje = tk.Label(self, text="", bg=NEGRO, font=(FUENTE, 10, "bold"))
        self._lbl_mensaje.pack(pady=(10, 0))

    @abstractmethod
    def construir_widgets(self):
        pass

    @abstractmethod
    def validar(self):
        pass

    @abstractmethod
    def limpiar(self):
        pass

    def mostrar_mensaje(self, texto, ok=False):
        self._lbl_mensaje.config(text=texto, fg=VERDE if ok else ROJO)

    # ---- widgets decorados que usan las pantallas hijas ----
    def titulo(self, texto):
        tk.Label(self, text=texto, bg=NEGRO, fg=MORADO_CLARO,
                 font=(FUENTE, 18, "bold")).pack(pady=(0, 10))

    def seccion(self, padre, texto):
        marco = tk.LabelFrame(padre, text=texto, bg=NEGRO, fg=MORADO_CLARO,
                              font=(FUENTE, 10, "bold"), padx=12, pady=10,
                              highlightbackground=MORADO, highlightthickness=1, bd=0)
        marco.pack(fill="x", pady=4)
        return marco

    def etiqueta(self, padre, texto, obligatorio=False):
        # los campos obligatorios se ven en lila y con asterisco
        color = LILA if obligatorio else BLANCO
        tk.Label(padre, text=texto, bg=NEGRO, fg=color,
                 font=(FUENTE, 9)).pack(anchor="w", pady=(6, 2))

    def entrada(self, padre, variable, ancho=32, oculto=False):
        caja = tk.Entry(padre, textvariable=variable, width=ancho,
                        show="*" if oculto else "", bg=GRIS, fg=BLANCO,
                        insertbackground=BLANCO, relief="flat",
                        highlightthickness=1, highlightbackground=GRIS,
                        highlightcolor=MORADO, font=(FUENTE, 10))
        caja.pack(anchor="w", ipady=4)
        return caja

    def boton(self, padre, texto, comando):
        tk.Button(padre, text=texto, command=comando, bg=MORADO, fg=BLANCO,
                  activebackground=MORADO_CLARO, activeforeground=NEGRO,
                  relief="flat", bd=0, padx=14, pady=6, cursor="hand2",
                  font=(FUENTE, 10, "bold")).pack(side="left", padx=4)

    def casilla(self, padre, texto, variable, lado="top"):
        tk.Checkbutton(padre, text=texto, variable=variable, bg=NEGRO, fg=BLANCO,
                       selectcolor=NEGRO, activebackground=NEGRO,
                       activeforeground=MORADO_CLARO,
                       font=(FUENTE, 9)).pack(side=lado, anchor="w", padx=(0, 8))

    def opcion(self, padre, texto, valor, variable):
        tk.Radiobutton(padre, text=texto, value=valor, variable=variable,
                       bg=NEGRO, fg=BLANCO, selectcolor=NEGRO,
                       activebackground=NEGRO, activeforeground=MORADO_CLARO,
                       font=(FUENTE, 9)).pack(side="left", padx=(0, 8))

    def lista_desplegable(self, padre, variable, valores):
        ttk.Combobox(padre, textvariable=variable, values=valores,
                     state="readonly", width=30).pack(anchor="w", ipady=2)


class VentanaLogin(VentanaBase):
    USUARIO_DEMO = "admin"   # solo para practicar
    CLAVE_DEMO = "1234"

    def construir_widgets(self):
        self._var_usuario = tk.StringVar()
        self._var_clave = tk.StringVar()
        self._var_recordar = tk.BooleanVar()

        self.titulo("Iniciar sesión")
        marco = self.seccion(self, "Acceso")

        self.etiqueta(marco, "Usuario o correo *", obligatorio=True)
        self.entrada(marco, self._var_usuario)

        self.etiqueta(marco, "Contraseña *", obligatorio=True)
        self.entrada(marco, self._var_clave, oculto=True)

        self.casilla(marco, "Recordar sesión", self._var_recordar)

        botones = tk.Frame(self, bg=NEGRO)
        botones.pack(pady=(12, 0))
        self.boton(botones, "Ingresar", self.ingresar)
        self.boton(botones, "Registrarse", self.ir_a_registro)
        self.boton(botones, "Limpiar", self.limpiar)

    def validar(self):
        if not self._var_usuario.get().strip() or not self._var_clave.get():
            self.mostrar_mensaje("Completa usuario y contraseña.")
            return False
        return True

    def limpiar(self):
        self._var_usuario.set("")
        self._var_clave.set("")
        self._var_recordar.set(False)
        self.mostrar_mensaje("")

    def ingresar(self):
        if not self.validar():
            return
        if (self._var_usuario.get().strip() == self.USUARIO_DEMO
                and self._var_clave.get() == self.CLAVE_DEMO):
            self.mostrar_mensaje("¡Bienvenido al sistema!", ok=True)
        else:
            self.mostrar_mensaje("Usuario o contraseña incorrectos.")

    def ir_a_registro(self):
        self.app.mostrar_registro()