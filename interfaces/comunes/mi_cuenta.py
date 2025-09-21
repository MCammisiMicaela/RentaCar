import tkinter as tk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from recursos.estilos import *
from servicios.autenticacion import validar_registro
from servicios.validaciones import validar_cambio_contraseña
import json, os

RUTA_USUARIOS = os.path.join("datos", "usuarios.json")

def mostrar_mi_cuenta(usuario_actual, ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.deiconify()
    ventana.title("Mi cuenta - RentaCar")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    # Fondo
    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize(TAMANIO_FONDO)
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar fondo:", e)

    # Cargar datos actuales
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
            usuarios = json.load(archivo)
    except:
        usuarios = {}

    datos_actuales = usuarios.get(usuario_actual, {})

    # Frame principal
    frame = tk.Frame(ventana, bg=COLOR_FONDO, width=800, height=800)
    frame.place(x=30, y=20)

    y_actual = 10

    # Título
    tk.Label(frame, text="Modificar datos personales", **CONFIG_LABEL_TITULO).place(x=30, y=y_actual)
    y_actual += 50

    def campo(label_texto, valor, estado="normal"):
        nonlocal y_actual
        tk.Label(frame, text=label_texto, **CONFIG_LABEL_FORMULARIO).place(x=30, y=y_actual)
        entrada = tk.Entry(frame, **CONFIG_ENTRY)
        entrada.place(x=250, y=y_actual)
        entrada.insert(0, valor)
        entrada.config(state=estado)
        y_actual += 40
        return entrada

    entrada_nombre = campo("Nombre:", datos_actuales.get("nombre", ""))
    entrada_apellido = campo("Apellido:", datos_actuales.get("apellido", ""))
    tk.Label(frame, text="Fecha de nacimiento:", **CONFIG_LABEL_FORMULARIO).place(x=30, y=y_actual)
    entrada_fecha = DateEntry(frame, **CONFIG_FECHA)
    entrada_fecha.place(x=250, y=y_actual)
    entrada_fecha.set_date(datos_actuales.get("fecha_nacimiento", "01/01/2000"))
    y_actual += 40
    entrada_celular = campo("Celular:", datos_actuales.get("celular", ""))
    entrada_usuario = campo("Nombre de usuario:", usuario_actual, estado="disabled")

    mensaje_datos = tk.Label(frame, text="", **CONFIG_MENSAJE)
    mensaje_datos.place(x=30, y=y_actual)

    def guardar_datos_personales():
        nuevos_datos = {
            "nombre": entrada_nombre.get().strip(),
            "apellido": entrada_apellido.get().strip(),
            "fecha_nacimiento": entrada_fecha.get_date(),
            "celular": entrada_celular.get().strip(),
            "usuario": usuario_actual,
            "contraseña": datos_actuales.get("contraseña"),
            "confirmar_contraseña": datos_actuales.get("contraseña"),
            "tipo": datos_actuales.get("tipo"),
            "bloqueado": datos_actuales.get("bloqueado", False)
        }

        estado, mensajes = validar_registro(nuevos_datos, {usuario_actual: datos_actuales}, modo="edicion")
        if not estado:
            mensaje_datos.config(text=mensajes[0], fg=COLOR_ERROR)
            return

        nuevos_datos["fecha_nacimiento"] = nuevos_datos["fecha_nacimiento"].strftime("%d/%m/%Y")
        usuarios[usuario_actual].update(nuevos_datos)

        with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo:
            json.dump(usuarios, archivo, indent=4)

        mensaje_datos.config(text="Datos actualizados correctamente.", fg=COLOR_EXITO)

    tk.Button(frame, text="Guardar cambios", command=guardar_datos_personales, **CONFIG_BOTON_FORMULARIO).place(x=550, y=y_actual - 40)
    y_actual += 50

    # Sección contraseña
    tk.Label(frame, text="Cambiar contraseña", **CONFIG_LABEL_TITULO).place(x=30, y=y_actual)
    y_actual += 50

    def campo_password(label_texto):
        nonlocal y_actual
        tk.Label(frame, text=label_texto, **CONFIG_LABEL_FORMULARIO).place(x=30, y=y_actual)
        entrada = tk.Entry(frame, show="*", **CONFIG_ENTRY)
        entrada.place(x=250, y=y_actual)
        y_actual += 40
        return entrada

    entrada_actual = campo_password("Contraseña actual:")
    entrada_nueva = campo_password("Nueva contraseña:")
    entrada_confirmacion = campo_password("Confirmar nueva contraseña:")

    mensaje_contrasenia = tk.Label(frame, text="", **CONFIG_MENSAJE)
    mensaje_contrasenia.place(x=30, y=y_actual)

    def cambiar_contrasenia():
        actual = entrada_actual.get()
        nueva = entrada_nueva.get()
        confirmacion = entrada_confirmacion.get()

        estado, mensaje = validar_cambio_contraseña(
            actual=actual,
            nueva=nueva,
            confirmacion=confirmacion,
            contraseña_guardada=datos_actuales.get("contraseña")
        )

        if not estado:
            mensaje_contrasenia.config(text=mensaje, fg=COLOR_ERROR)
            return

        usuarios[usuario_actual]["contraseña"] = nueva
        with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo:
            json.dump(usuarios, archivo, indent=4)

        mensaje_contrasenia.config(text="Contraseña actualizada correctamente.", fg=COLOR_EXITO)

    tk.Button(frame, text="Cambiar contraseña", command=cambiar_contrasenia, **CONFIG_BOTON_FORMULARIO).place(x=550, y=y_actual - 40)

    # Botón volver abajo centrado
    def volver():
        if datos_actuales.get("tipo") == "admin":
            from interfaces.administrador.menu_admin import mostrar_menu_admin
            mostrar_menu_admin(usuario_actual, ventana)
        else:
            from interfaces.cliente.menu_cliente import mostrar_menu_cliente
            mostrar_menu_cliente(usuario_actual, ventana)

    tk.Button(ventana, text="Volver", command=volver, **CONFIG_BOTON_FORMULARIO).place(relx=0.5, rely=0.95, anchor="center")