import tkinter as tk
from PIL import Image, ImageTk
from recursos.estilos import *
from servicios.autenticacion import validar_registro
import json, os

RUTA_USUARIOS = os.path.join("datos", "usuarios.json")

def mostrar_registro_cliente():
    # Usamos Toplevel para no romper el contexto gráfico
    ventana = tk.Toplevel()
    ventana.title("RentaCar - Registro de cliente")
    ventana.geometry("800x600")
    ventana.resizable(False, False)

    # Cargar imagen de fondo
    try:
        imagen_original = Image.open(RUTA_FONDO_LIMPIO)
        imagen_redimensionada = imagen_original.resize((800, 600))
        fondo_img = ImageTk.PhotoImage(imagen_redimensionada)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        ventana.fondo_img = fondo_img  # mantiene la imagen viva
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar la imagen de fondo:", e)

    # Campos de entrada
    campos = {
        "nombre": tk.Entry(ventana, width=30),
        "apellido": tk.Entry(ventana, width=30),
        "fecha_nacimiento": tk.Entry(ventana, width=30),
        "celular": tk.Entry(ventana, width=30),
        "usuario": tk.Entry(ventana, width=30),
        "contraseña": tk.Entry(ventana, width=30, show="*"),
        "confirmar_contraseña": tk.Entry(ventana, width=30, show="*")
    }

    etiquetas = [
        ("Nombre:", "nombre", 140),
        ("Apellido:", "apellido", 180),
        ("Fecha de nacimiento:", "fecha_nacimiento", 220),
        ("Celular:", "celular", 260),
        ("Nombre de usuario:", "usuario", 300),
        ("Contraseña:", "contraseña", 340),
        ("Confirmar contraseña:", "confirmar_contraseña", 380)
    ]

    for texto, clave, y in etiquetas:
        tk.Label(ventana, text=texto, font=TIPO_LETRA,
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=200, y=y)
        campos[clave].place(x=400, y=y)

    # Mensaje dinámico
    mensaje_label = tk.Label(ventana, text="", font=TIPO_LETRA, bg=COLOR_FONDO)
    mensaje_label.place(x=400, y=420)

    # Acción del botón registrar
    def registrar_cliente():
        datos = {clave: campo.get().strip() for clave, campo in campos.items()}
        datos["tipo"] = "cliente"
        datos["bloqueado"] = False

        try:
            with open(RUTA_USUARIOS, "r") as archivo:
                usuarios = json.load(archivo)
        except:
            usuarios = {}

        estado, mensajes = validar_registro(datos, usuarios)

        if not estado:
            mensaje_label.config(text=mensajes[0], fg=COLOR_ERROR)
            return

        usuarios[datos["usuario"]] = {
            "nombre": datos["nombre"],
            "apellido": datos["apellido"],
            "fecha_nacimiento": datos["fecha_nacimiento"],
            "celular": datos["celular"],
            "usuario": datos["usuario"],
            "contraseña": datos["contraseña"],
            "tipo": "cliente",
            "bloqueado": False
        }

        with open(RUTA_USUARIOS, "w") as archivo:
            json.dump(usuarios, archivo, indent=4)

        mensaje_label.config(text=mensajes[0], fg=COLOR_EXITO)
        ventana.after(1500, ventana.destroy)

    # Botón Registrar
    btn_registrar = tk.Button(
        ventana,
        text="Crear cuenta",
        font=TIPO_LETRA,
        bg=COLOR_BOTON,
        fg=COLOR_TEXTO_BOTON,
        width=15,
        command=registrar_cliente
    )
    btn_registrar.place(relx=0.5, y=460, anchor="center")


