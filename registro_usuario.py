import tkinter as tk
from datetime import datetime
from inicio_sesion import VentanaBase, NEGRO, GRIS, BLANCO, MORADO, MORADO_CLARO, FUENTE


class Cliente:
    # los datos van privados (con __) y solo se leen por las properties

    def __init__(self, nombre, tipo_doc, num_doc, fecha_nac, genero,
                 intereses, ciudad, direccion, observaciones, satisfaccion):
        self.__nombre = nombre
        self.__tipo_doc = tipo_doc
        self.__num_doc = num_doc
        self.__fecha_nac = fecha_nac
        self.__genero = genero
        self.__intereses = intereses
        self.__ciudad = ciudad
        self.__direccion = direccion
        self.__observaciones = observaciones
        self.__satisfaccion = satisfaccion

    @property
    def nombre(self):
        return self.__nombre

    @property
    def num_doc(self):
        return self.__num_doc

    @property
    def ciudad(self):
        return self.__ciudad

    def resumen(self):
        return f"{self.__nombre} ({self.__tipo_doc} {self.__num_doc}) - {self.__ciudad}"


class VentanaRegistro(VentanaBase):
    TIPOS_DOC = ["Cédula de ciudadanía", "Tarjeta de identidad", "Pasaporte"]
    CIUDADES = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga", "Cucutá"]
    INTERESES = ["Deportes", "Tecnología", "Música", "Viajes"]

    def construir_widgets(self):
        self._var_nombre = tk.StringVar()
        self._var_tipo_doc = tk.StringVar()
        self._var_num_doc = tk.StringVar()
        self._var_fecha = tk.StringVar()
        self._var_genero = tk.StringVar()
        self._var_ciudad = tk.StringVar()
        self._var_direccion = tk.StringVar()
        self._var_satisfaccion = tk.IntVar(value=5)
        self._vars_intereses = {i: tk.BooleanVar() for i in self.INTERESES}

        self.titulo("Registro de clientes")

        # dos columnas para que la ventana no quede tan larga
        columnas = tk.Frame(self, bg=NEGRO)
        columnas.pack()
        izq = tk.Frame(columnas, bg=NEGRO)
        izq.pack(side="left", anchor="n", padx=6)
        der = tk.Frame(columnas, bg=NEGRO)
        der.pack(side="left", anchor="n", padx=6)

        # ---- columna izquierda: datos personales ----
        personales = self.seccion(izq, "Datos personales")

        self.etiqueta(personales, "Nombre completo *", obligatorio=True)
        self.entrada(personales, self._var_nombre)

        self.etiqueta(personales, "Tipo de documento *", obligatorio=True)
        self.lista_desplegable(personales, self._var_tipo_doc, self.TIPOS_DOC)

        self.etiqueta(personales, "Número de documento *", obligatorio=True)
        self.entrada(personales, self._var_num_doc)

        self.etiqueta(personales, "Fecha de nacimiento (AAAA-MM-DD) *", obligatorio=True)
        self.entrada(personales, self._var_fecha)

        self.etiqueta(personales, "Género *", obligatorio=True)
        fila_genero = tk.Frame(personales, bg=NEGRO)
        fila_genero.pack(anchor="w")
        for texto in ("Femenino", "Masculino", "Otro"):
            self.opcion(fila_genero, texto, texto, self._var_genero)

        # ---- columna derecha: contacto y preferencias ----
        contacto = self.seccion(der, "Contacto")

        self.etiqueta(contacto, "Ciudad *", obligatorio=True)
        self.lista_desplegable(contacto, self._var_ciudad, self.CIUDADES)

        self.etiqueta(contacto, "Dirección")
        self.entrada(contacto, self._var_direccion)

        prefs = self.seccion(der, "Preferencias")

        self.etiqueta(prefs, "Intereses (puedes marcar varios)")
        fila_intereses = tk.Frame(prefs, bg=NEGRO)
        fila_intereses.pack(anchor="w")
        for nombre, var in self._vars_intereses.items():
            self.casilla(fila_intereses, nombre, var, lado="left")

        self.etiqueta(prefs, "Nivel de satisfacción (1-10)")
        tk.Scale(prefs, from_=1, to=10, orient="horizontal",
                 variable=self._var_satisfaccion, length=220, bg=NEGRO, fg=BLANCO,
                 troughcolor=MORADO, activebackground=MORADO_CLARO,
                 highlightthickness=0, bd=0).pack(anchor="w")

        self.etiqueta(prefs, "Observaciones")
        self._txt_obs = tk.Text(prefs, width=30, height=3, bg=GRIS, fg=BLANCO,
                                insertbackground=BLANCO, relief="flat",
                                highlightthickness=1, highlightbackground=GRIS,
                                highlightcolor=MORADO, font=(FUENTE, 10))
        self._txt_obs.pack(anchor="w")

        # ---- botones de abajo ----
        botones = tk.Frame(self, bg=NEGRO)
        botones.pack(pady=(12, 0))
        self.boton(botones, "Guardar", self.guardar)
        self.boton(botones, "Limpiar", self.limpiar)
        self.boton(botones, "Volver", self.volver)

    def validar(self):
        if not self._var_nombre.get().strip():
            self.mostrar_mensaje("El nombre es obligatorio.")
            return False
        if not self._var_tipo_doc.get():
            self.mostrar_mensaje("Elige el tipo de documento.")
            return False
        if not self._var_num_doc.get().strip().isdigit():
            self.mostrar_mensaje("El número de documento solo puede tener dígitos.")
            return False
        try:
            datetime.strptime(self._var_fecha.get().strip(), "%Y-%m-%d")
        except ValueError:
            self.mostrar_mensaje("Fecha inválida, usa el formato AAAA-MM-DD.")
            return False
        if not self._var_genero.get():
            self.mostrar_mensaje("Elige el género.")
            return False
        if not self._var_ciudad.get():
            self.mostrar_mensaje("Elige la ciudad.")
            return False
        return True

    def limpiar(self):
        for var in (self._var_nombre, self._var_tipo_doc, self._var_num_doc,
                    self._var_fecha, self._var_genero, self._var_ciudad,
                    self._var_direccion):
            var.set("")
        for var in self._vars_intereses.values():
            var.set(False)
        self._var_satisfaccion.set(5)
        self._txt_obs.delete("1.0", "end")
        self.mostrar_mensaje("")

    def guardar(self):
        if not self.validar():
            return
        intereses = [n for n, v in self._vars_intereses.items() if v.get()]
        cliente = Cliente(
            self._var_nombre.get().strip(),
            self._var_tipo_doc.get(),
            self._var_num_doc.get().strip(),
            self._var_fecha.get().strip(),
            self._var_genero.get(),
            intereses,
            self._var_ciudad.get(),
            self._var_direccion.get().strip(),
            self._txt_obs.get("1.0", "end-1c").strip(),
            self._var_satisfaccion.get(),
        )
        self.app.clientes.append(cliente)
        self.limpiar()
        self.mostrar_mensaje(f"Cliente guardado: {cliente.nombre}", ok=True)

    def volver(self):
        self.app.mostrar_login()