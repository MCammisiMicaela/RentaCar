import tkinter as tk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from recursos.estilos import *
from servicios.autenticacion import validar_registro
from servicios.validaciones import validar_cambio_contraseña
from servicios.gestion_usuarios import cargar_usuarios, guardar_usuarios
from servicios.seguridad import crear_hash_contrasena

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

    entrada_nombre = campo("Nombre:", usuario_actual.nombre)
    entrada_apellido = campo("Apellido:", usuario_actual.apellido)
    tk.Label(frame, text="Fecha de nacimiento:", **CONFIG_LABEL_FORMULARIO).place(x=30, y=y_actual)
    entrada_fecha = DateEntry(frame, **CONFIG_FECHA)
    entrada_fecha.place(x=250, y=y_actual)
    entrada_fecha.set_date(usuario_actual.fecha_nacimiento)
    y_actual += 40
    entrada_celular = campo("Celular:", usuario_actual.celular)
    entrada_usuario = campo("Nombre de usuario:", usuario_actual.usuario, estado="disabled")

    mensaje_datos = tk.Label(frame, text="", **CONFIG_MENSAJE)
    mensaje_datos.place(x=30, y=y_actual)

    def guardar_datos_personales():
        nuevos_datos = {
            "nombre": entrada_nombre.get().strip(),
            "apellido": entrada_apellido.get().strip(),
            "fecha_nacimiento": entrada_fecha.get_date(),
            "celular": entrada_celular.get().strip(),
            "usuario": usuario_actual.usuario,
            "contraseña": usuario_actual.contraseña,
            "confirmar_contraseña": usuario_actual.contraseña,
            "tipo": usuario_actual.tipo,
            "bloqueado": usuario_actual.bloqueado
        }

        estado, mensajes = validar_registro(nuevos_datos, [usuario_actual.usuario], modo="edicion")
        if not estado:
            mensaje_datos.config(text=mensajes[0], fg=COLOR_ERROR)
            return

        # Actualiza atributos del objeto
        usuario_actual.nombre = nuevos_datos["nombre"]
        usuario_actual.apellido = nuevos_datos["apellido"]
        usuario_actual.fecha_nacimiento = nuevos_datos["fecha_nacimiento"].strftime("%d/%m/%Y") \
            if hasattr(nuevos_datos["fecha_nacimiento"], "strftime") else nuevos_datos["fecha_nacimiento"]
        usuario_actual.celular = nuevos_datos["celular"]

        # Guarda todos los usuarios
        usuarios = cargar_usuarios()
        for i, u in enumerate(usuarios):
            if u.usuario == usuario_actual.usuario:
                usuarios[i] = usuario_actual
                break
        guardar_usuarios(usuarios)

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
            contraseña_guardada=usuario_actual.contraseña
        )

        if not estado:
            mensaje_contrasenia.config(text=mensaje, fg=COLOR_ERROR)
            return

        # Guardar un hash, nunca la contraseña original.
        usuario_actual.contraseña = crear_hash_contrasena(nueva)
        usuarios = cargar_usuarios()
        for i, u in enumerate(usuarios):
            if u.usuario == usuario_actual.usuario:
                usuarios[i] = usuario_actual
                break
        guardar_usuarios(usuarios)

        mensaje_contrasenia.config(text="Contraseña actualizada correctamente.", fg=COLOR_EXITO)

    tk.Button(frame, text="Cambiar contraseña", command=cambiar_contrasenia, **CONFIG_BOTON_FORMULARIO).place(x=550, y=y_actual - 40)

    # Botón volver abajo centrado
    def volver():
        if usuario_actual.tipo == "admin":
            from interfaces.administrador.menu_admin import mostrar_menu_admin
            mostrar_menu_admin(usuario_actual, ventana)
        else:
            from interfaces.cliente.menu_cliente import mostrar_menu_cliente
            mostrar_menu_cliente(usuario_actual, ventana)

    tk.Button(ventana, text="Volver", command=volver, **CONFIG_BOTON_FORMULARIO).place(relx=0.5, rely=0.95, anchor="center")