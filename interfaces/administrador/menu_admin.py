import tkinter as tk
from PIL import Image, ImageTk
from recursos.estilos import *

def mostrar_menu_admin():
    ventana = tk.Toplevel()
    ventana.title("RentaCar - Sistema administrativo")
    ventana.geometry("800x600")
    ventana.resizable(False, False)

    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize((800, 600))
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar fondo:", e)

    # Encabezado 
    tk.Label(ventana, text="Sistema administrativo de gestión", font=TIPO_LETRA,
             bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=30, y=140)

    # Botones de gestión
    botones_izquierda = [
        ("Clientes", lambda: print("Ir a Clientes")),
        ("Administradores", lambda: print("Ir a Administradores")),
        ("Historial de reservas", lambda: print("Ir a Historial")),
        ("Gestión de autos", lambda: print("Ir a Gestión de autos")),
        ("Agregar auto", lambda: print("Ir a Agregar auto"))
    ]

    for i, (texto, comando) in enumerate(botones_izquierda):
        tk.Button(
            ventana,
            text=texto,
            font=TIPO_LETRA,
            bg=COLOR_BOTON,
            fg=COLOR_FONDO,
            activebackground=COLOR_HOVER_BOTON_CLARO,
            width=20,
            height=2,
            bd=0,
            command=comando
        ).place(x=50, y=220 + i * 60)

    # Botones de cuenta personal
    tk.Button(
        ventana,
        text="Mi cuenta",
        font=TIPO_LETRA,
        bg=COLOR_BOTON,
        fg=COLOR_FONDO,
        activebackground=COLOR_HOVER_BOTON_CLARO,
        width=15,
        height=2,
        bd=0,
        command=lambda: print("Ir a Mi cuenta")
    ).place(x=600, y=200)

    tk.Button(
        ventana,
        text="Cerrar sesión",
        font=TIPO_LETRA,
        bg=COLOR_BOTON,
        fg=COLOR_FONDO,
        activebackground=COLOR_HOVER_BOTON_CLARO,
        width=15,
        height=2,
        bd=0,
        command=ventana.destroy
    ).place(x=600, y=260)