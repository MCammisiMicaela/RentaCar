import tkinter as tk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from recursos.estilos import *

def mostrar_menu_cliente():
    ventana = tk.Toplevel()
    ventana.title("RentaCar - Alquiler de autos")
    ventana.geometry("800x600")
    ventana.resizable(False, False)

    # Fondo
    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize((800, 600))
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar fondo:", e)

    # Encabezado
    tk.Label(ventana, text="Alquiler de autos", font=("Segoe UI", 24, "bold"),
             bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=30, y=140)

    tk.Label(ventana, text="Ubi: Terminal de colectivos, Esperanza", font=TIPO_LETRA,
             bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=30, y=200)

    # Botón Mi cuenta
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

    # Botón Mis reservas 
    tk.Button(
        ventana,
        text="Mis reservas",
        font=TIPO_LETRA,
        bg=COLOR_BOTON,
        fg=COLOR_FONDO,
        activebackground=COLOR_HOVER_BOTON_CLARO,
        width=15,  # igual que los otros
        height=2,
        bd=0,
        command=lambda: print("Ir a Mis reservas")
    ).place(x=600, y=260)

    # Botón Cerrar sesión
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
    ).place(x=600, y=320)

    # Selector de fechas
    tk.Label(ventana, text="Fecha de entrega:", font=TIPO_LETRA,
             bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=50, y=400)
    fecha_entrega = DateEntry(ventana, width=12, background=COLOR_BOTON,
                              foreground=COLOR_FONDO, borderwidth=0, date_pattern='dd/mm/yyyy')
    fecha_entrega.place(x=200, y=400)

    tk.Label(ventana, text="Fecha de devolución:", font=TIPO_LETRA,
             bg=COLOR_FONDO, fg=COLOR_TEXTO).place(x=50, y=440)
    fecha_devolucion = DateEntry(ventana, width=12, background=COLOR_BOTON,
                                 foreground=COLOR_FONDO, borderwidth=0, date_pattern='dd/mm/yyyy')
    fecha_devolucion.place(x=200, y=440)

    # Botón Buscar
    tk.Button(
        ventana,
        text="Buscar",
        font=TIPO_LETRA,
        bg=COLOR_BOTON,
        fg=COLOR_FONDO,
        activebackground=COLOR_HOVER_BOTON_CLARO,
        width=15,
        height=2,
        bd=0,
        command=lambda: print("Buscar autos entre", fecha_entrega.get(), "y", fecha_devolucion.get())
    ).place(x=600, y=500)