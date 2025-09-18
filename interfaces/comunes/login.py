import tkinter as tk
from PIL import Image, ImageTk
from recursos.estilos import *
from servicios.autenticacion import validar_login
from interfaces.cliente.registro_cliente import mostrar_registro_cliente
from interfaces.administrador.menu_admin import mostrar_menu_admin
from interfaces.cliente.menu_cliente import mostrar_menu_cliente

def mostrar_login():
    ventana = tk.Tk()
    ventana.title("RentaCar - Inicio de sesión")
    ventana.geometry("800x600")
    ventana.resizable(False, False)

    # Fondo
    imagen_original = Image.open(RUTA_FONDO)
    imagen_redimensionada = imagen_original.resize((800, 600))
    fondo_img = ImageTk.PhotoImage(imagen_redimensionada)
    fondo_label = tk.Label(ventana, image=fondo_img)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Campos
    tk.Label(ventana, text="Usuario:", font=TIPO_LETRA, bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=250, y=220)
    entry_usuario = tk.Entry(ventana, width=30)
    entry_usuario.place(x=350, y=220)

    tk.Label(ventana, text="Contraseña:", font=TIPO_LETRA, bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=250, y=260)
    entry_contraseña = tk.Entry(ventana, width=30, show="*")
    entry_contraseña.place(x=350, y=260)

    # Mensaje dinámico
    mensaje_label = tk.Label(ventana, text="", font=TIPO_LETRA, bg=COLOR_FONDO)
    mensaje_label.place(x=350, y=290)

    # Acción del botón login
    def intentar_login():
        usuario = entry_usuario.get().strip()
        contraseña = entry_contraseña.get().strip()

        estado, mensaje, tipo = validar_login(usuario, contraseña)

        if not estado:
            mensaje_label.config(text=mensaje, fg=COLOR_ERROR)
            return

        mensaje_label.config(text=mensaje, fg=COLOR_EXITO)
        ventana.withdraw() # oculta la ventana de login

        # Redirección por tipo
        if tipo == "admin":
            mostrar_menu_admin()
        elif tipo == "cliente":
            mostrar_menu_cliente()
        else:
            print("Tipo de usuario desconocido.")

    # Botón Iniciar sesión
    btn_login = tk.Button(ventana, text="Iniciar sesión", font=TIPO_LETRA, bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=15, command=intentar_login)
    btn_login.place(x=350, y=320)

    # Botón Registrarse (puede abrir otra ventana)
    btn_registro = tk.Button(ventana, text="Registrarse", font=TIPO_LETRA, bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON, width=15, command=mostrar_registro_cliente)
    btn_registro.place(x=350, y=370)

    ventana.mainloop()