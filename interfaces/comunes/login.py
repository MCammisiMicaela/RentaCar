import tkinter as tk
from PIL import Image, ImageTk
from recursos.estilos import *
from servicios.autenticacion import validar_login
from interfaces.comunes.registro_usuario import mostrar_registro_usuario
from interfaces.administrador.menu_admin import mostrar_menu_admin
from interfaces.cliente.menu_cliente import mostrar_menu_cliente

def mostrar_login(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.deiconify()
    ventana.title("RentaCar - Inicio de sesión")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    # Fondo
    fondo = Image.open(RUTA_FONDO).resize(TAMANIO_FONDO)
    fondo_img = ImageTk.PhotoImage(fondo)
    fondo_label = tk.Label(ventana, image=fondo_img)
    fondo_label.image = fondo_img
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    fondo_label.lower()  # Envía el fondo al fondo de la pila de widgets

    tk.Label(ventana, text="Usuario:", **CONFIG_LABEL_FORMULARIO).place(x=250, y=220)
    tk.Label(ventana, text="Contraseña:", **CONFIG_LABEL_FORMULARIO).place(x=250, y=260)

    # Campos
    campos = {
        "usuario": tk.Entry(ventana, **CONFIG_ENTRY),
        "contrasenia": tk.Entry(ventana, show="*", **CONFIG_ENTRY)
        }
    
    campos["usuario"].place(x=350, y=220)
    campos["contrasenia"].place(x=350, y=260)

    # Mensaje dinámico
    mensaje_label = tk.Label(ventana, text="", **CONFIG_MENSAJE)
    mensaje_label.place(x=350, y=290)

    # Acción del botón "Iniciar sesión"
    def intentar_login():
        usuario = campos["usuario"].get().strip()
        contraseña = campos["contrasenia"].get().strip()

        estado, mensaje, tipo = validar_login(usuario, contraseña) # Autenticación

        if not estado: 
            mensaje_label.config(text=mensaje, fg=COLOR_ERROR)
            return

        mensaje_label.config(text=mensaje, fg=COLOR_EXITO)
        ventana.withdraw() # oculta la ventana de login

        if tipo == "admin":
            mostrar_menu_admin(usuario, ventana)
        elif tipo == "cliente":
            mostrar_menu_cliente(lambda: mostrar_login(ventana))
        else:
            print("Tipo de usuario desconocido.")

    # Botones
    tk.Button(ventana, text="Iniciar sesión", command=intentar_login, **CONFIG_BOTON_FORMULARIO).place(x=350, y=320)

    def mostrar_registro_cliente():
        mostrar_registro_usuario(
            tipo_usuario="cliente",
            titulo="Registro de cliente",
            mensaje_exito="Cuenta creada correctamente.", 
            ventana = ventana
        )

    tk.Button(ventana, text="Registrarse", command=mostrar_registro_cliente, **CONFIG_BOTON_FORMULARIO).place(x=350, y=370)



