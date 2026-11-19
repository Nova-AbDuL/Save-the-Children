# Sistema de voluntariado y donaciones - Save the Children Bolivia
# Prototipo academico (datos ficticios)
# Python + tkinter + ttkbootstrap + MySQL

import os
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

import ttkbootstrap as ttk
import mysql.connector
from PIL import Image, ImageTk

# ------------------------------------------------------------
# CONFIGURACION (cambiar con los datos de tu MySQL)
# ------------------------------------------------------------
CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "voluntariado_db",   # <- nombre de tu base de datos
}

# Nombres de los estados que tienes guardados en tus tablas de estado.
# Si en tu base se llaman distinto, solo cambialos aqui.
EST_VOL_PENDIENTE = "Pendiente"
EST_VOL_APROBADO = "Aprobado"
EST_VOL_RECHAZADO = "Rechazado"
EST_POS_PENDIENTE = "Pendiente"
EST_POS_APROBADA = "Aprobada"
EST_POS_RECHAZADA = "Rechazada"
EST_ACT_INICIAL = "Programada"

# Colores
ROJO = "#B8282F"
ROJO_OSCURO = "#8A1A22"
ROJO_CLARO = "#F6DEDD"
FONDO = "#FBF6F4"
BLANCO = "#FFFFFF"
TEXTO = "#2B1B1D"
GRIS = "#7A6B6D"

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_USUARIO = os.path.join(CARPETA, "usuario_recordado.txt")

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


# ------------------------------------------------------------
# FUNCIONES DE BASE DE DATOS
# ------------------------------------------------------------
def conectar():
    return mysql.connector.connect(**CONFIG)


def consultar(sql, params=()):
    """Ejecuta un SELECT y devuelve todas las filas."""
    con = conectar()
    cur = con.cursor()
    cur.execute(sql, params)
    filas = cur.fetchall()
    cur.close()
    con.close()
    return filas


def ejecutar(sql, params=()):
    """Ejecuta INSERT / UPDATE / DELETE y devuelve el ultimo id."""
    con = conectar()
    cur = con.cursor()
    cur.execute(sql, params)
    con.commit()
    nuevo_id = cur.lastrowid
    cur.close()
    con.close()
    return nuevo_id


def id_estado(tabla, campo_id, nombre):
    """Busca el id de un estado por su nombre."""
    filas = consultar("SELECT " + campo_id + " FROM " + tabla + " WHERE nombre = %s", (nombre,))
    if filas:
        return filas[0][0]
    return None


def fecha_hoy_texto():
    hoy = datetime.date.today()
    return DIAS[hoy.weekday()] + " " + str(hoy.day) + " de " + MESES[hoy.month - 1] + " de " + str(hoy.year)


# ------------------------------------------------------------
# VENTANA PRINCIPAL
# ------------------------------------------------------------
class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Sistema de voluntariado y donaciones - Save the Children Bolivia")
        self.geometry("1150x700")
        self.minsize(1000, 640)
        self.fotos = []            # guardamos las imagenes para que no se borren
        self.id_usuario = None
        self.nombre_usuario = ""
        self.es_admin = False
        self.id_voluntario = None
        self.mostrar_login()

    def limpiar(self):
        for w in self.winfo_children():
            w.destroy()
        self.fotos = []

    # --------------------------------------------------------
    # LOGO (carga la imagen de la carpeta "imagenes")
    # --------------------------------------------------------
    def poner_logo(self, padre, archivo, ancho, fondo, color_texto, tam_texto):
        ruta = os.path.join(CARPETA, "imagenes", archivo)
        try:
            img = Image.open(ruta).convert("RGBA")
            alto = int(img.height * ancho / img.width)
            img = img.resize((ancho, alto))
            foto = ImageTk.PhotoImage(img)
            self.fotos.append(foto)
            return tk.Label(padre, image=foto, bg=fondo)
        except Exception:
            # si no encuentra la imagen, muestra solo el nombre
            return tk.Label(padre, text="Save the Children", bg=fondo, fg=color_texto,
                            font=("Segoe UI", tam_texto, "bold"))

    # --------------------------------------------------------
    # PANTALLA DE LOGIN
    # --------------------------------------------------------
    def mostrar_login(self):
        self.limpiar()
        self.id_usuario = None

        izq = tk.Frame(self, bg=ROJO, width=480)
        izq.pack(side="left", fill="y")
        izq.pack_propagate(False)

        self.poner_logo(izq, "logo_blanco.png", 330, ROJO, "white", 22).pack(anchor="w", padx=50, pady=(150, 60))
        tk.Label(izq, text="Voluntariado y donaciones", bg=ROJO, fg="white",
                 font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=50)
        tk.Label(izq, text="Gestiona tu participación en las actividades\ny apoya a la niñez de Bolivia.",
                 bg=ROJO, fg="white", font=("Segoe UI", 12), justify="left").pack(anchor="w", padx=50, pady=15)
        tk.Label(izq, text="  Prototipo académico · datos ficticios  ", bg=ROJO_OSCURO, fg="white",
                 font=("Segoe UI", 9)).pack(side="bottom", anchor="w", padx=50, pady=30)

        der = tk.Frame(self, bg=FONDO)
        der.pack(side="right", fill="both", expand=True)

        tarjeta = tk.Frame(der, bg=BLANCO, highlightbackground="#EADDDA", highlightthickness=1)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center", width=430, height=520)

        tk.Label(tarjeta, text="Bienvenido", bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 24, "bold")).pack(anchor="w", padx=30, pady=(30, 0))
        tk.Label(tarjeta, text="Inicia sesión para continuar", bg=BLANCO, fg=GRIS,
                 font=("Segoe UI", 10)).pack(anchor="w", padx=30)

        tk.Label(tarjeta, text="Usuario", bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=30, pady=(20, 3))
        self.var_usuario = tk.StringVar()
        ttk.Entry(tarjeta, textvariable=self.var_usuario, font=("Segoe UI", 11)).pack(fill="x", padx=30)

        tk.Label(tarjeta, text="Contraseña", bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=30, pady=(15, 3))
        fila_pass = tk.Frame(tarjeta, bg=BLANCO)
        fila_pass.pack(fill="x", padx=30)
        self.var_pass = tk.StringVar()
        self.entry_pass = ttk.Entry(fila_pass, textvariable=self.var_pass, show="•", font=("Segoe UI", 11))
        self.entry_pass.pack(side="left", fill="x", expand=True)
        ttk.Button(fila_pass, text="👁", width=3, bootstyle="secondary-outline",
                   command=self.ver_password).pack(side="left", padx=(5, 0))

        self.var_recordar = tk.BooleanVar(value=False)
        ttk.Checkbutton(tarjeta, text="Recordar usuario", variable=self.var_recordar,
                        bootstyle="danger").pack(anchor="w", padx=30, pady=15)

        ttk.Button(tarjeta, text="Ingresar", bootstyle="danger", command=self.iniciar_sesion).pack(fill="x", padx=30, ipady=6)

        fila_reg = tk.Frame(tarjeta, bg=BLANCO)
        fila_reg.pack(pady=12)
        tk.Label(fila_reg, text="¿Aún no eres voluntario?", bg=BLANCO, fg=GRIS).pack(side="left")
        lbl = tk.Label(fila_reg, text=" Regístrate", bg=BLANCO, fg=ROJO, cursor="hand2",
                       font=("Segoe UI", 10, "bold"))
        lbl.pack(side="left")
        lbl.bind("<Button-1>", lambda e: self.ventana_registro())

        ttk.Separator(tarjeta).pack(fill="x", padx=30, pady=5)

        caja = tk.Frame(tarjeta, bg="#FCF4F2", highlightbackground="#EADDDA", highlightthickness=1)
        caja.pack(fill="x", padx=30, pady=10)
        tk.Label(caja, text="♡", bg=ROJO_CLARO, fg=ROJO, font=("Segoe UI", 18)).pack(side="left", padx=10, pady=10)
        textos = tk.Frame(caja, bg="#FCF4F2")
        textos.pack(side="left")
        tk.Label(textos, text="Realizar una donación", bg="#FCF4F2", fg=TEXTO,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(textos, text="No necesitas iniciar sesión", bg="#FCF4F2", fg=GRIS,
                 font=("Segoe UI", 8)).pack(anchor="w")
        ttk.Button(caja, text="Donar ahora", bootstyle="danger-outline",
                   command=self.ventana_donacion).pack(side="right", padx=10)

        # Si habia un usuario recordado lo ponemos
        if os.path.exists(ARCHIVO_USUARIO):
            with open(ARCHIVO_USUARIO, "r") as f:
                self.var_usuario.set(f.read().strip())
                self.var_recordar.set(True)

        self.bind("<Return>", lambda e: self.iniciar_sesion())

    def ver_password(self):
        if self.entry_pass.cget("show") == "":
            self.entry_pass.config(show="•")
        else:
            self.entry_pass.config(show="")

    def iniciar_sesion(self):
        usuario = self.var_usuario.get().strip()
        clave = self.var_pass.get()
        if usuario == "" or clave == "":
            messagebox.showwarning("Faltan datos", "Escribe tu usuario y contraseña.")
            return
        try:
            filas = consultar(
                "SELECT u.id_usuario, u.usuario, r.nombre FROM usuario u "
                "JOIN rol r ON r.id_rol = u.id_rol "
                "WHERE u.usuario = %s AND u.contrasena = %s AND u.activo = 1",
                (usuario, clave))
            if not filas:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
                return

            self.id_usuario = filas[0][0]
            self.nombre_usuario = filas[0][1]
            self.es_admin = filas[0][2].lower().startswith("admin")
            self.id_voluntario = None

            if not self.es_admin:
                datos = consultar(
                    "SELECT v.id_voluntario, ev.nombre FROM voluntario v "
                    "JOIN estado_voluntario ev ON ev.id_estado_vol = v.id_estado_vol "
                    "WHERE v.id_usuario = %s", (self.id_usuario,))
                if not datos or datos[0][1] != EST_VOL_APROBADO:
                    messagebox.showinfo("Cuenta en revisión",
                                        "Tu registro aún no fue aprobado por un administrador.")
                    return
                self.id_voluntario = datos[0][0]
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return

        if self.var_recordar.get():
            with open(ARCHIVO_USUARIO, "w") as f:
                f.write(usuario)
        elif os.path.exists(ARCHIVO_USUARIO):
            os.remove(ARCHIVO_USUARIO)

        self.unbind("<Return>")
        self.mostrar_principal()

    # --------------------------------------------------------
    # REGISTRO DE VOLUNTARIO
    # --------------------------------------------------------
    def ventana_registro(self):
        win = ttk.Toplevel(self)
        win.title("Registro de voluntario")
        win.geometry("400x560")
        campos = ["Nombres", "Apellidos", "Cédula", "Correo", "Teléfono", "Usuario", "Contraseña"]
        entradas = {}
        for c in campos:
            ttk.Label(win, text=c).pack(anchor="w", padx=30, pady=(10, 0))
            e = ttk.Entry(win, show="•" if c == "Contraseña" else "")
            e.pack(fill="x", padx=30)
            entradas[c] = e

        def guardar():
            d = {c: entradas[c].get().strip() for c in campos}
            if "" in d.values():
                messagebox.showwarning("Faltan datos", "Completa todos los campos.", parent=win)
                return
            try:
                if consultar("SELECT id_usuario FROM usuario WHERE usuario = %s", (d["Usuario"],)):
                    messagebox.showerror("Error", "Ese usuario ya existe.", parent=win)
                    return
                if consultar("SELECT id_voluntario FROM voluntario WHERE cedula = %s", (d["Cédula"],)):
                    messagebox.showerror("Error", "Esa cédula ya está registrada.", parent=win)
                    return
                rol = consultar("SELECT id_rol FROM rol WHERE LOWER(nombre) LIKE 'volunt%'")
                if not rol:
                    messagebox.showerror("Error", "No existe el rol Voluntario en la tabla rol.", parent=win)
                    return
                est = id_estado("estado_voluntario", "id_estado_vol", EST_VOL_PENDIENTE)
                nuevo = ejecutar("INSERT INTO usuario (id_rol, usuario, contrasena, activo) VALUES (%s, %s, %s, 1)",
                                 (rol[0][0], d["Usuario"], d["Contraseña"]))
                ejecutar("INSERT INTO voluntario (id_usuario, id_estado_vol, nombres, apellidos, cedula, "
                         "correo, telefono, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())",
                         (nuevo, est, d["Nombres"], d["Apellidos"], d["Cédula"], d["Correo"], d["Teléfono"]))
                messagebox.showinfo("Listo", "Registro enviado. Espera la aprobación del administrador.", parent=win)
                win.destroy()
            except mysql.connector.Error as error:
                messagebox.showerror("Error de base de datos", str(error), parent=win)

        ttk.Button(win, text="Registrarme", bootstyle="danger", command=guardar).pack(pady=20)

    # --------------------------------------------------------
    # VENTANA DE DONACION (sin iniciar sesion)
    # --------------------------------------------------------
    def ventana_donacion(self, despues=None):
        win = ttk.Toplevel(self)
        win.title("Realizar una donación")
        win.geometry("400x560")

        etiquetas = ["Nombres", "Correo", "Teléfono", "Monto (Bs.)", "Observación"]
        entradas = {}
        for c in etiquetas:
            ttk.Label(win, text=c).pack(anchor="w", padx=30, pady=(10, 0))
            e = ttk.Entry(win)
            e.pack(fill="x", padx=30)
            entradas[c] = e

        ttk.Label(win, text="Método de pago").pack(anchor="w", padx=30, pady=(10, 0))
        try:
            metodos = consultar("SELECT id_metodo_pago, nombre FROM metodo_pago")
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error), parent=win)
            win.destroy()
            return
        combo = ttk.Combobox(win, values=[m[1] for m in metodos], state="readonly")
        combo.pack(fill="x", padx=30)
        if metodos:
            combo.current(0)

        def guardar():
            nombres = entradas["Nombres"].get().strip()
            correo = entradas["Correo"].get().strip()
            telefono = entradas["Teléfono"].get().strip()
            obs = entradas["Observación"].get().strip()
            try:
                monto = float(entradas["Monto (Bs.)"].get().replace(",", "."))
            except ValueError:
                messagebox.showwarning("Monto", "Escribe un monto válido.", parent=win)
                return
            if nombres == "" or monto <= 0 or combo.get() == "":
                messagebox.showwarning("Faltan datos", "Completa nombre, monto y método de pago.", parent=win)
                return
            id_metodo = metodos[combo.current()][0]
            try:
                donante = consultar("SELECT id_donante FROM donante WHERE correo = %s", (correo,))
                if donante and correo != "":
                    id_donante = donante[0][0]
                else:
                    id_donante = ejecutar("INSERT INTO donante (nombres, correo, telefono) VALUES (%s, %s, %s)",
                                          (nombres, correo, telefono))
                ejecutar("INSERT INTO donacion (id_donante, id_metodo_pago, monto, fecha, observacion) "
                         "VALUES (%s, %s, %s, CURDATE(), %s)", (id_donante, id_metodo, monto, obs))
                messagebox.showinfo("¡Gracias!", "Tu donación fue registrada.", parent=win)
                win.destroy()
                if despues:
                    despues()
            except mysql.connector.Error as error:
                messagebox.showerror("Error de base de datos", str(error), parent=win)

        ttk.Button(win, text="Donar", bootstyle="danger", command=guardar).pack(pady=20)

    # --------------------------------------------------------
    # PANTALLA PRINCIPAL (menu lateral + contenido)
    # --------------------------------------------------------
    def mostrar_principal(self):
        self.limpiar()

        self.sidebar = tk.Frame(self, bg=ROJO, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.poner_logo(self.sidebar, "logo_blanco.png", 190, ROJO, "white", 14).pack(pady=(25, 20))
        tk.Label(self.sidebar, text="MENÚ", bg=ROJO, fg="#F0C4C6", font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=20)

        if self.es_admin:
            opciones = [("Panel", self.pagina_panel), ("Voluntarios", self.pagina_voluntarios),
                        ("Actividades", self.pagina_actividades), ("Postulaciones", self.pagina_postulaciones),
                        ("Asistencia", self.pagina_asistencia), ("Donaciones", self.pagina_donaciones),
                        ("Reportes", self.pagina_reportes)]
        else:
            opciones = [("Actividades", self.pagina_actividades_vol),
                        ("Mis postulaciones", self.pagina_mis_postulaciones)]

        self.botones_menu = {}
        for texto, funcion in opciones:
            b = tk.Button(self.sidebar, text="   " + texto, anchor="w", bg=ROJO, fg="white",
                          activebackground="#A9454B", activeforeground="white", bd=0, relief="flat",
                          font=("Segoe UI", 11), cursor="hand2",
                          command=lambda f=funcion, t=texto: self.ir_a(f, t))
            b.pack(fill="x", padx=12, pady=3, ipady=7)
            self.botones_menu[texto] = b

        pie = tk.Frame(self.sidebar, bg=ROJO_OSCURO)
        pie.pack(side="bottom", fill="x", padx=12, pady=15)
        rol = "Administrador" if self.es_admin else "Voluntario"
        tk.Label(pie, text=self.nombre_usuario, bg=ROJO_OSCURO, fg="white", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
        tk.Label(pie, text=rol, bg=ROJO_OSCURO, fg="#F0C4C6", font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=(0, 8))
        tk.Button(self.sidebar, text="— Cerrar sesión", bg=ROJO, fg="white", bd=0, activebackground=ROJO,
                  activeforeground="white", cursor="hand2", command=self.mostrar_login).pack(side="bottom", anchor="w", padx=20)

        derecha = tk.Frame(self, bg=FONDO)
        derecha.pack(side="right", fill="both", expand=True)

        # encabezado
        self.encabezado = tk.Frame(derecha, bg=BLANCO)
        self.encabezado.pack(fill="x")
        self.lbl_titulo = tk.Label(self.encabezado, text="", bg=BLANCO, fg=TEXTO, font=("Segoe UI", 18, "bold"))
        self.lbl_titulo.grid(row=0, column=0, sticky="w", padx=25, pady=(12, 0))
        self.lbl_sub = tk.Label(self.encabezado, text="", bg=BLANCO, fg=GRIS, font=("Segoe UI", 9))
        self.lbl_sub.grid(row=1, column=0, sticky="w", padx=25, pady=(0, 10))
        self.encabezado.columnconfigure(0, weight=1)

        if self.es_admin:
            self.var_buscar = tk.StringVar()
            buscador = ttk.Entry(self.encabezado, textvariable=self.var_buscar, width=30)
            buscador.grid(row=0, column=1, rowspan=2, padx=20)
            buscador.bind("<Return>", lambda e: self.pagina_voluntarios(self.var_buscar.get().strip()))
            tk.Label(self.encabezado, text="Buscar voluntario (Enter)", bg=BLANCO, fg=GRIS,
                     font=("Segoe UI", 7)).grid(row=1, column=1, sticky="s")

        self.contenido = tk.Frame(derecha, bg=FONDO)
        self.contenido.pack(fill="both", expand=True, padx=25, pady=15)

        primera = opciones[0]
        self.ir_a(primera[1], primera[0])

    def ir_a(self, funcion, texto):
        for t, b in self.botones_menu.items():
            b.config(bg=ROJO)
        self.botones_menu[texto].config(bg="#B34A50")
        funcion()

    def preparar(self, titulo, subtitulo):
        for w in self.contenido.winfo_children():
            w.destroy()
        self.lbl_titulo.config(text=titulo)
        self.lbl_sub.config(text=subtitulo)

    def tarjeta(self, padre):
        return tk.Frame(padre, bg=BLANCO, highlightbackground="#EADDDA", highlightthickness=1)

    # --------------------------------------------------------
    # PANEL DEL ADMINISTRADOR
    # --------------------------------------------------------
    def pagina_panel(self):
        self.preparar("Panel del administrador", fecha_hoy_texto() + "  ·  Resumen general del voluntariado")
        try:
            activos = consultar("SELECT COUNT(*) FROM voluntario v JOIN estado_voluntario e ON e.id_estado_vol = v.id_estado_vol WHERE e.nombre = %s", (EST_VOL_APROBADO,))[0][0]
            pendientes = consultar("SELECT COUNT(*) FROM voluntario v JOIN estado_voluntario e ON e.id_estado_vol = v.id_estado_vol WHERE e.nombre = %s", (EST_VOL_PENDIENTE,))[0][0]
            horas = consultar("SELECT COALESCE(SUM(horas), 0) FROM asistencia WHERE asistio = 1")[0][0]
            total_don, cant_don = consultar("SELECT COALESCE(SUM(monto), 0), COUNT(*) FROM donacion")[0]
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return

        # tarjetas de arriba
        fila = tk.Frame(self.contenido, bg=FONDO)
        fila.pack(fill="x")
        datos = [("Voluntarios activos", str(activos), "Aprobados en el sistema", ROJO),
                 ("Pendientes de aprobar", str(pendientes), "Requieren tu revisión", "#B7791F"),
                 ("Horas de voluntariado", str(int(horas)) + " h", "Acumuladas", "#2F855A"),
                 ("Donaciones", "Bs. " + str(int(total_don)), str(cant_don) + " donaciones", ROJO)]
        for i, (t, v, n, color) in enumerate(datos):
            c = self.tarjeta(fila)
            c.grid(row=0, column=i, sticky="nsew", padx=5)
            fila.columnconfigure(i, weight=1)
            tk.Label(c, text=t, bg=BLANCO, fg=GRIS, font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(12, 0))
            tk.Label(c, text=v, bg=BLANCO, fg=TEXTO, font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=15)
            tk.Label(c, text=n, bg=BLANCO, fg=color, font=("Segoe UI", 8)).pack(anchor="w", padx=15, pady=(0, 12))

        medio = tk.Frame(self.contenido, bg=FONDO)
        medio.pack(fill="both", expand=True, pady=10)
        medio.columnconfigure(0, weight=3)
        medio.columnconfigure(1, weight=2)
        medio.rowconfigure(0, weight=1)
        medio.rowconfigure(1, weight=1)

        # voluntarios pendientes
        c1 = self.tarjeta(medio)
        c1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tk.Label(c1, text="Voluntarios pendientes de aprobación", bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 5))
        pend = consultar("SELECT v.id_voluntario, CONCAT(v.nombres, ' ', v.apellidos), v.cedula, v.fecha_registro "
                         "FROM voluntario v JOIN estado_voluntario e ON e.id_estado_vol = v.id_estado_vol "
                         "WHERE e.nombre = %s ORDER BY v.fecha_registro LIMIT 3", (EST_VOL_PENDIENTE,))
        if not pend:
            tk.Label(c1, text="No hay voluntarios pendientes", bg=BLANCO, fg=GRIS).pack(pady=20)
        for p in pend:
            f = tk.Frame(c1, bg=BLANCO)
            f.pack(fill="x", padx=15, pady=4)
            tk.Label(f, text=p[1], bg=BLANCO, fg=TEXTO, font=("Segoe UI", 10, "bold"), width=22, anchor="w").pack(side="left")
            tk.Label(f, text=p[2], bg=BLANCO, fg=GRIS, width=10).pack(side="left")
            tk.Label(f, text=str(p[3]), bg=BLANCO, fg=GRIS, width=11).pack(side="left")
            ttk.Button(f, text="✕", width=3, bootstyle="danger-outline",
                       command=lambda i=p[0]: self.resolver_voluntario(i, EST_VOL_RECHAZADO)).pack(side="right")
            ttk.Button(f, text="Aprobar", bootstyle="success",
                       command=lambda i=p[0]: self.resolver_voluntario(i, EST_VOL_APROBADO)).pack(side="right", padx=5)

        # proximas actividades
        c2 = self.tarjeta(medio)
        c2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        tk.Label(c2, text="Próximas actividades", bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 5))
        acts = consultar("SELECT a.id_actividad, a.nombre, a.lugar, a.fecha, a.cupo, "
                         "(SELECT COUNT(*) FROM postulacion p JOIN estado_postulacion ep ON ep.id_estado_pos = p.id_estado_pos "
                         " WHERE p.id_actividad = a.id_actividad AND ep.nombre = %s) "
                         "FROM actividad a WHERE a.fecha >= CURDATE() ORDER BY a.fecha LIMIT 3", (EST_POS_APROBADA,))
        if not acts:
            tk.Label(c2, text="No hay actividades próximas", bg=BLANCO, fg=GRIS).pack(pady=20)
        for a in acts:
            f = tk.Frame(c2, bg=BLANCO)
            f.pack(fill="x", padx=15, pady=4)
            tk.Label(f, text=str(a[3].day) + "\n" + MESES[a[3].month - 1][:3].upper(), bg=ROJO_CLARO, fg=ROJO,
                     font=("Segoe UI", 10, "bold"), width=5).pack(side="left", padx=(0, 10))
            info = tk.Frame(f, bg=BLANCO)
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=a[1], bg=BLANCO, fg=TEXTO, font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(info, text=a[2], bg=BLANCO, fg=GRIS, font=("Segoe UI", 8)).pack(anchor="w")
            cupo = a[4] if a[4] else 1
            ttk.Progressbar(info, maximum=cupo, value=a[5], bootstyle="danger").pack(fill="x")
            tk.Label(f, text=str(a[5]) + "/" + str(a[4]), bg=BLANCO, fg=GRIS).pack(side="right", padx=5)

        # voluntarios con mas horas
        c3 = self.tarjeta(medio)
        c3.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tk.Label(c3, text="Voluntarios con más horas", bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 5))
        top = consultar("SELECT CONCAT(v.nombres, ' ', v.apellidos), SUM(a.horas), COUNT(*) "
                        "FROM asistencia a JOIN postulacion p ON p.id_postulacion = a.id_postulacion "
                        "JOIN voluntario v ON v.id_voluntario = p.id_voluntario "
                        "WHERE a.asistio = 1 GROUP BY v.id_voluntario ORDER BY SUM(a.horas) DESC LIMIT 4")
        mayor = float(top[0][1]) if top else 1
        for n, t in enumerate(top, start=1):
            f = tk.Frame(c3, bg=BLANCO)
            f.pack(fill="x", padx=15, pady=3)
            tk.Label(f, text=str(n), bg=ROJO_CLARO, fg=ROJO, width=3).pack(side="left")
            tk.Label(f, text=t[0], bg=BLANCO, fg=TEXTO, width=20, anchor="w").pack(side="left", padx=5)
            ttk.Progressbar(f, maximum=mayor, value=float(t[1]), bootstyle="danger").pack(side="left", fill="x", expand=True)
            tk.Label(f, text=str(int(t[1])) + " h · " + str(t[2]) + " act.", bg=BLANCO, fg=GRIS).pack(side="right", padx=5)

        # donaciones recientes
        c4 = self.tarjeta(medio)
        c4.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        tk.Label(c4, text="Donaciones recientes", bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 5))
        dons = consultar("SELECT d.nombres, m.nombre, c.monto FROM donacion c "
                         "JOIN donante d ON d.id_donante = c.id_donante "
                         "JOIN metodo_pago m ON m.id_metodo_pago = c.id_metodo_pago "
                         "ORDER BY c.fecha DESC, c.id_donacion DESC LIMIT 3")
        for d in dons:
            f = tk.Frame(c4, bg=BLANCO)
            f.pack(fill="x", padx=15, pady=4)
            tk.Label(f, text=d[1], bg=ROJO_CLARO, fg=ROJO, font=("Segoe UI", 8), width=9).pack(side="left")
            tk.Label(f, text=d[0], bg=BLANCO, fg=TEXTO, font=("Segoe UI", 10, "bold")).pack(side="left", padx=8)
            tk.Label(f, text="Bs. " + str(d[2]), bg=BLANCO, fg=TEXTO, font=("Segoe UI", 10, "bold")).pack(side="right")

    def resolver_voluntario(self, id_vol, estado):
        try:
            nuevo = id_estado("estado_voluntario", "id_estado_vol", estado)
            ejecutar("UPDATE voluntario SET id_estado_vol = %s, id_admin_aprueba = %s WHERE id_voluntario = %s",
                     (nuevo, self.id_usuario, id_vol))
            nombre = consultar("SELECT CONCAT(nombres, ' ', apellidos) FROM voluntario WHERE id_voluntario = %s", (id_vol,))[0][0]
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        messagebox.showinfo("Listo", "Voluntario " + estado.lower() + ": " + nombre)
        self.pagina_panel()

    # --------------------------------------------------------
    # TABLA GENERICA (la usan casi todas las paginas)
    # --------------------------------------------------------
    def crear_tabla(self, columnas, filas, anchos=None):
        caja = self.tarjeta(self.contenido)
        caja.pack(fill="both", expand=True)
        tree = ttk.Treeview(caja, columns=columnas, show="headings", bootstyle="danger")
        for i, c in enumerate(columnas):
            tree.heading(c, text=c)
            tree.column(c, width=anchos[i] if anchos else 120, anchor="w")
        for f in filas:
            tree.insert("", "end", iid=str(f[0]), values=[str(x) if x is not None else "" for x in f[1:]])
        scroll = ttk.Scrollbar(caja, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        return tree

    def barra_botones(self, botones, tree):
        barra = tk.Frame(self.contenido, bg=FONDO)
        barra.pack(fill="x", pady=(0, 8))
        for texto, estilo, funcion in botones:
            ttk.Button(barra, text=texto, bootstyle=estilo,
                       command=lambda f=funcion: self.con_seleccion(tree, f)).pack(side="left", padx=(0, 8))

    def con_seleccion(self, tree, funcion):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona una fila", "Primero selecciona un registro de la tabla.")
            return
        funcion(int(sel[0]))

    # --------------------------------------------------------
    # VOLUNTARIOS
    # --------------------------------------------------------
    def pagina_voluntarios(self, filtro=""):
        self.preparar("Voluntarios", "Lista de voluntarios registrados")
        sql = ("SELECT v.id_voluntario, CONCAT(v.nombres, ' ', v.apellidos), v.cedula, v.correo, v.telefono, "
               "v.fecha_registro, e.nombre FROM voluntario v JOIN estado_voluntario e ON e.id_estado_vol = v.id_estado_vol")
        params = ()
        if filtro != "":
            sql += " WHERE v.nombres LIKE %s OR v.apellidos LIKE %s OR v.cedula LIKE %s"
            params = ("%" + filtro + "%",) * 3
        sql += " ORDER BY v.fecha_registro DESC"
        try:
            filas = consultar(sql, params)
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        tabla = self.crear_tabla(["Nombre", "Cédula", "Correo", "Teléfono", "Registro", "Estado"], filas,
                                 [200, 90, 200, 100, 100, 100])
        self.barra_botones([("Aprobar", "success", lambda i: self.resolver_voluntario_lista(i, EST_VOL_APROBADO)),
                            ("Rechazar", "danger-outline", lambda i: self.resolver_voluntario_lista(i, EST_VOL_RECHAZADO))],
                           tabla)

    def resolver_voluntario_lista(self, id_vol, estado):
        try:
            nuevo = id_estado("estado_voluntario", "id_estado_vol", estado)
            ejecutar("UPDATE voluntario SET id_estado_vol = %s, id_admin_aprueba = %s WHERE id_voluntario = %s",
                     (nuevo, self.id_usuario, id_vol))
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        self.pagina_voluntarios()

    # --------------------------------------------------------
    # ACTIVIDADES
    # --------------------------------------------------------
    def pagina_actividades(self):
        self.preparar("Actividades", "Actividades de voluntariado")
        try:
            filas = consultar("SELECT a.id_actividad, a.nombre, a.fecha, a.hora_inicio, a.hora_fin, a.lugar, a.cupo, e.nombre "
                              "FROM actividad a JOIN estado_actividad e ON e.id_estado_act = a.id_estado_act ORDER BY a.fecha DESC")
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        barra = tk.Frame(self.contenido, bg=FONDO)
        barra.pack(fill="x", pady=(0, 8))
        ttk.Button(barra, text="+ Nueva actividad", bootstyle="danger", command=self.ventana_actividad).pack(side="left")
        self.crear_tabla(["Nombre", "Fecha", "Inicio", "Fin", "Lugar", "Cupo", "Estado"], filas,
                         [200, 90, 70, 70, 160, 60, 100])

    def ventana_actividad(self):
        win = ttk.Toplevel(self)
        win.title("Nueva actividad")
        win.geometry("400x560")
        campos = ["Nombre", "Descripción", "Fecha (AAAA-MM-DD)", "Hora inicio (HH:MM)", "Hora fin (HH:MM)", "Lugar", "Cupo"]
        ent = {}
        for c in campos:
            ttk.Label(win, text=c).pack(anchor="w", padx=30, pady=(10, 0))
            e = ttk.Entry(win)
            e.pack(fill="x", padx=30)
            ent[c] = e

        def guardar():
            d = {c: ent[c].get().strip() for c in campos}
            if "" in d.values() or not d["Cupo"].isdigit():
                messagebox.showwarning("Datos", "Completa todo y el cupo debe ser un número.", parent=win)
                return
            try:
                est = id_estado("estado_actividad", "id_estado_act", EST_ACT_INICIAL)
                if est is None:
                    est = consultar("SELECT MIN(id_estado_act) FROM estado_actividad")[0][0]
                ejecutar("INSERT INTO actividad (id_estado_act, nombre, descripcion, fecha, hora_inicio, hora_fin, lugar, cupo) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                         (est, d["Nombre"], d["Descripción"], d["Fecha (AAAA-MM-DD)"], d["Hora inicio (HH:MM)"],
                          d["Hora fin (HH:MM)"], d["Lugar"], int(d["Cupo"])))
            except mysql.connector.Error as error:
                messagebox.showerror("Error de base de datos", str(error), parent=win)
                return
            win.destroy()
            self.pagina_actividades()

        ttk.Button(win, text="Guardar", bootstyle="danger", command=guardar).pack(pady=20)

    # --------------------------------------------------------
    # POSTULACIONES
    # --------------------------------------------------------
    def pagina_postulaciones(self):
        self.preparar("Postulaciones", "Voluntarios que se postularon a actividades")
        try:
            filas = consultar("SELECT p.id_postulacion, CONCAT(v.nombres, ' ', v.apellidos), a.nombre, a.fecha, "
                              "p.fecha_postulacion, ep.nombre FROM postulacion p "
                              "JOIN voluntario v ON v.id_voluntario = p.id_voluntario "
                              "JOIN actividad a ON a.id_actividad = p.id_actividad "
                              "JOIN estado_postulacion ep ON ep.id_estado_pos = p.id_estado_pos "
                              "ORDER BY p.fecha_postulacion DESC")
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        tabla = self.crear_tabla(["Voluntario", "Actividad", "Fecha actividad", "Postulación", "Estado"], filas,
                                 [200, 200, 110, 110, 100])
        self.barra_botones([("Aprobar", "success", lambda i: self.resolver_postulacion(i, EST_POS_APROBADA)),
                            ("Rechazar", "danger-outline", lambda i: self.resolver_postulacion(i, EST_POS_RECHAZADA))],
                           tabla)

    def resolver_postulacion(self, id_pos, estado):
        try:
            nuevo = id_estado("estado_postulacion", "id_estado_pos", estado)
            ejecutar("UPDATE postulacion SET id_estado_pos = %s, id_admin_resuelve = %s WHERE id_postulacion = %s",
                     (nuevo, self.id_usuario, id_pos))
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        self.pagina_postulaciones()

    # --------------------------------------------------------
    # ASISTENCIA
    # --------------------------------------------------------
    def pagina_asistencia(self):
        self.preparar("Asistencia", "Registro de asistencia y horas (solo postulaciones aprobadas)")
        try:
            filas = consultar("SELECT p.id_postulacion, CONCAT(v.nombres, ' ', v.apellidos), a.nombre, a.fecha, "
                              "CASE WHEN s.asistio = 1 THEN 'Asistió' WHEN s.asistio = 0 THEN 'No asistió' ELSE 'Sin registrar' END, "
                              "COALESCE(s.horas, 0) FROM postulacion p "
                              "JOIN voluntario v ON v.id_voluntario = p.id_voluntario "
                              "JOIN actividad a ON a.id_actividad = p.id_actividad "
                              "JOIN estado_postulacion ep ON ep.id_estado_pos = p.id_estado_pos "
                              "LEFT JOIN asistencia s ON s.id_postulacion = p.id_postulacion "
                              "WHERE ep.nombre = %s ORDER BY a.fecha DESC", (EST_POS_APROBADA,))
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        tabla = self.crear_tabla(["Voluntario", "Actividad", "Fecha", "Asistencia", "Horas"], filas,
                                 [200, 200, 100, 110, 70])
        self.barra_botones([("Marcar asistió", "success", self.marcar_asistio),
                            ("Marcar no asistió", "danger-outline", self.marcar_no_asistio)], tabla)

    def guardar_asistencia(self, id_pos, asistio, horas):
        try:
            existe = consultar("SELECT id_asistencia FROM asistencia WHERE id_postulacion = %s", (id_pos,))
            if existe:
                ejecutar("UPDATE asistencia SET asistio = %s, horas = %s WHERE id_postulacion = %s", (asistio, horas, id_pos))
            else:
                ejecutar("INSERT INTO asistencia (id_postulacion, asistio, horas) VALUES (%s, %s, %s)", (id_pos, asistio, horas))
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        self.pagina_asistencia()

    def marcar_asistio(self, id_pos):
        horas = simpledialog.askfloat("Horas", "¿Cuántas horas hizo el voluntario?", minvalue=0, maxvalue=24)
        if horas is None:
            return
        self.guardar_asistencia(id_pos, 1, horas)

    def marcar_no_asistio(self, id_pos):
        self.guardar_asistencia(id_pos, 0, 0)

    # --------------------------------------------------------
    # DONACIONES
    # --------------------------------------------------------
    def pagina_donaciones(self):
        self.preparar("Donaciones", "Historial de donaciones")
        try:
            filas = consultar("SELECT c.id_donacion, d.nombres, d.correo, m.nombre, c.monto, c.fecha, c.observacion "
                              "FROM donacion c JOIN donante d ON d.id_donante = c.id_donante "
                              "JOIN metodo_pago m ON m.id_metodo_pago = c.id_metodo_pago ORDER BY c.fecha DESC, c.id_donacion DESC")
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        barra = tk.Frame(self.contenido, bg=FONDO)
        barra.pack(fill="x", pady=(0, 8))
        ttk.Button(barra, text="+ Nueva donación", bootstyle="danger",
                   command=lambda: self.ventana_donacion(self.pagina_donaciones)).pack(side="left")
        self.crear_tabla(["Donante", "Correo", "Método", "Monto (Bs.)", "Fecha", "Observación"], filas,
                         [180, 180, 100, 90, 100, 200])

    # --------------------------------------------------------
    # REPORTES
    # --------------------------------------------------------
    def pagina_reportes(self):
        self.preparar("Reportes", "Resumen de la información del sistema")
        try:
            por_estado = consultar("SELECT e.nombre, COUNT(v.id_voluntario) FROM estado_voluntario e "
                                   "LEFT JOIN voluntario v ON v.id_estado_vol = e.id_estado_vol GROUP BY e.id_estado_vol")
            por_act = consultar("SELECT a.nombre, COALESCE(SUM(s.horas), 0) FROM actividad a "
                                "LEFT JOIN postulacion p ON p.id_actividad = a.id_actividad "
                                "LEFT JOIN asistencia s ON s.id_postulacion = p.id_postulacion AND s.asistio = 1 "
                                "GROUP BY a.id_actividad")
            por_metodo = consultar("SELECT m.nombre, COALESCE(SUM(c.monto), 0) FROM metodo_pago m "
                                   "LEFT JOIN donacion c ON c.id_metodo_pago = m.id_metodo_pago GROUP BY m.id_metodo_pago")
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return

        texto = "VOLUNTARIOS POR ESTADO\n"
        for n, c in por_estado:
            texto += "   - " + n + ": " + str(c) + "\n"
        texto += "\nHORAS POR ACTIVIDAD\n"
        for n, h in por_act:
            texto += "   - " + n + ": " + str(h) + " h\n"
        texto += "\nDONACIONES POR MÉTODO DE PAGO\n"
        for n, m in por_metodo:
            texto += "   - " + n + ": Bs. " + str(m) + "\n"

        caja = self.tarjeta(self.contenido)
        caja.pack(fill="both", expand=True)
        tk.Label(caja, text=texto, bg=BLANCO, fg=TEXTO, justify="left", anchor="nw",
                 font=("Consolas", 11)).pack(fill="both", expand=True, padx=20, pady=15)

    # --------------------------------------------------------
    # VISTA DEL VOLUNTARIO
    # --------------------------------------------------------
    def pagina_actividades_vol(self):
        self.preparar("Actividades disponibles", "Elige una actividad y postúlate")
        try:
            filas = consultar("SELECT a.id_actividad, a.nombre, a.fecha, a.hora_inicio, a.hora_fin, a.lugar, a.cupo "
                              "FROM actividad a WHERE a.fecha >= CURDATE() ORDER BY a.fecha")
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        tabla = self.crear_tabla(["Nombre", "Fecha", "Inicio", "Fin", "Lugar", "Cupo"], filas, [220, 90, 70, 70, 180, 60])
        self.barra_botones([("Postularme", "danger", self.postularme)], tabla)

    def postularme(self, id_act):
        try:
            ya = consultar("SELECT id_postulacion FROM postulacion WHERE id_voluntario = %s AND id_actividad = %s",
                           (self.id_voluntario, id_act))
            if ya:
                messagebox.showinfo("Aviso", "Ya te postulaste a esta actividad.")
                return
            est = id_estado("estado_postulacion", "id_estado_pos", EST_POS_PENDIENTE)
            ejecutar("INSERT INTO postulacion (id_voluntario, id_actividad, id_estado_pos, fecha_postulacion) "
                     "VALUES (%s, %s, %s, CURDATE())", (self.id_voluntario, id_act, est))
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        messagebox.showinfo("Listo", "Tu postulación fue enviada.")

    def pagina_mis_postulaciones(self):
        self.preparar("Mis postulaciones", "Estado de tus postulaciones y horas acumuladas")
        try:
            filas = consultar("SELECT p.id_postulacion, a.nombre, a.fecha, ep.nombre, COALESCE(s.horas, 0) "
                              "FROM postulacion p JOIN actividad a ON a.id_actividad = p.id_actividad "
                              "JOIN estado_postulacion ep ON ep.id_estado_pos = p.id_estado_pos "
                              "LEFT JOIN asistencia s ON s.id_postulacion = p.id_postulacion "
                              "WHERE p.id_voluntario = %s ORDER BY a.fecha DESC", (self.id_voluntario,))
        except mysql.connector.Error as error:
            messagebox.showerror("Error de base de datos", str(error))
            return
        self.crear_tabla(["Actividad", "Fecha", "Estado", "Horas"], filas, [240, 100, 120, 80])


if __name__ == "__main__":
    app = App()
    app.mainloop()
