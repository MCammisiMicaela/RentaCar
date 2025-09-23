import tkinter as tk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from recursos.estilos import *
from servicios.autenticacion import validar_registro
from servicios.gestion_usuarios import cargar_usuarios, guardar_usuarios
from clases.cliente import Cliente
from clases.administrador import Administrador

def construir_formulario_usuario(ventana, y_inicial=150):
    """
    Construye todos los campos comunes para crear un usuario.
    Devuelve un diccionario con los widgets.
    """
    campos = {
        "nombre": tk.Entry(ventana, **CONFIG_ENTRY),
        "apellido": tk.Entry(ventana, **CONFIG_ENTRY),
        "fecha_nacimiento": DateEntry(ventana, **CONFIG_FECHA),
        "celular": tk.Entry(ventana, **CONFIG_ENTRY),
        "usuario": tk.Entry(ventana, **CONFIG_ENTRY),
        "contraseña": tk.Entry(ventana, show="*", **CONFIG_ENTRY),
        "confirmar_contraseña": tk.Entry(ventana, show="*", **CONFIG_ENTRY)
    }

    etiquetas = [
        ("Nombre:", "nombre"),
        ("Apellido:", "apellido"),
        ("Fecha de nacimiento:", "fecha_nacimiento"),
        ("Celular:", "celular"),
        ("Nombre de usuario:", "usuario"),
        ("Contraseña:", "contraseña"),
        ("Confirmar contraseña:", "confirmar_contraseña")
    ]

    for i, (texto, clave) in enumerate(etiquetas):
        y = y_inicial + i * 50
        tk.Label(ventana, text=texto, **CONFIG_LABEL_FORMULARIO).place(x=200, y=y)
        campos[clave].place(x=400, y=y)

    return campos

def mostrar_registro_usuario(tipo_usuario="cliente", titulo="Registro de usuario", mensaje_exito="Cuenta creada correctamente.", ventana=None, usuario_actual=None):
    for widget in ventana.winfo_children():
        widget.destroy()
    
    ventana.deiconify()
    ventana.title(f"RentaCar - {titulo}")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    # Fondo
    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize(TAMANIO_FONDO)
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        ventana.fondo_img = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar la imagen de fondo:", e)

        # Campos
    campos = construir_formulario_usuario(ventana)

    # Mensaje dinámico
    mensaje_label = tk.Label(ventana, text="", **CONFIG_MENSAJE)
    mensaje_label.place(x=400, y=480)

    def registrar_usuario():
        from interfaces.comunes.login import mostrar_login
        datos = {}
        for clave, campo in campos.items():
            datos[clave] = campo.get_date() if clave == "fecha_nacimiento" else campo.get().strip()

        datos["tipo"] = tipo_usuario
        datos["bloqueado"] = False

        usuarios = cargar_usuarios()
        usuarios_existentes = [u.usuario for u in usuarios]

        estado, mensajes = validar_registro(datos, usuarios_existentes)

        if not estado:
            mensaje_label.config(text=mensajes[0], fg=COLOR_ERROR)
            return
        
        datos.pop("confirmar_contraseña")
        # Formatea la fecha si es necesario
        if hasattr(datos["fecha_nacimiento"], "strftime"):
            datos["fecha_nacimiento"] = datos["fecha_nacimiento"].strftime("%d/%m/%Y")

        # Crear el objeto usuario
        if tipo_usuario == "admin":
            nuevo_usuario = Administrador(
                usuario=datos["usuario"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                fecha_nacimiento=datos["fecha_nacimiento"],
                celular=datos["celular"],
                contraseña=datos["contraseña"],
                tipo="admin",
                bloqueado=False
            )
        else:
            nuevo_usuario = Cliente(
                usuario=datos["usuario"],
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                fecha_nacimiento=datos["fecha_nacimiento"],
                celular=datos["celular"],
                contraseña=datos["contraseña"],
                tipo="cliente",
                bloqueado=False
            )

        usuarios.append(nuevo_usuario)
        guardar_usuarios(usuarios)

        mensaje_label.config(text=mensaje_exito, fg=COLOR_EXITO)

        ventana.after(1500, lambda: mostrar_login(ventana))

    def volver():
        if tipo_usuario == "admin":
            from interfaces.administrador.gestion_administradores import mostrar_gestion_administradores
            ventana.after(0, lambda: mostrar_gestion_administradores(usuario_actual, ventana))
        else:
            from interfaces.comunes.login import mostrar_login
            ventana.after(0, lambda: mostrar_login(ventana))

    tk.Button(ventana, text="Volver", command=volver, **CONFIG_BOTON_FORMULARIO).place(relx=0.5, y=570, anchor="center")
    tk.Button(ventana, text="Crear cuenta", command=registrar_usuario, **CONFIG_BOTON_FORMULARIO).place(relx=0.5, y=520, anchor="center")