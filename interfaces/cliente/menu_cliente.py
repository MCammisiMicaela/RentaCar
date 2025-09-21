import tkinter as tk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from recursos.estilos import *
from interfaces.comunes.mi_cuenta import mostrar_mi_cuenta

def mostrar_menu_cliente(usuario_actual, ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.deiconify()
    ventana.title("RentaCar - Alquiler de autos")
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

    # Encabezado
    tk.Label(ventana, text="Alquiler de autos", **CONFIG_LABEL_TITULO_GRANDE).place(x=30, y=140)
    tk.Label(ventana, text="Ubi: Terminal de colectivos, Esperanza", **CONFIG_LABEL_FORMULARIO).place(x=30, y=200)

    def cerrar_sesion():
        from interfaces.comunes.login import mostrar_login
        mostrar_login(ventana)

    # Botones de cuenta
    botones_derecha = [
        ("Mi cuenta", 200, lambda: mostrar_mi_cuenta(usuario_actual, ventana)),
        ("Mis reservas", 260, lambda: print("Ir a Mis reservas")),
        ("Cerrar sesión", 320, lambda: cerrar_sesion())
    ]

    for texto, y, comando in botones_derecha:
        tk.Button(ventana, text=texto, command=comando, **CONFIG_BOTON_FORMULARIO).place(x=600, y=y)

    # Selector de fechas
    tk.Label(ventana, text="Fecha de entrega:", **CONFIG_LABEL_FORMULARIO).place(x=50, y=400)
    fecha_entrega = DateEntry(ventana, **CONFIG_FECHA)
    fecha_entrega.place(x=200, y=400)

    tk.Label(ventana, text="Fecha de devolución:", **CONFIG_LABEL_FORMULARIO).place(x=50, y=440)
    fecha_devolucion = DateEntry(ventana, **CONFIG_FECHA)
    fecha_devolucion.place(x=200, y=440)

    # Botón Buscar
    tk.Button(
        ventana,
        text="Buscar",
        command=lambda: print("Buscar autos entre", fecha_entrega.get(), "y", fecha_devolucion.get()),
        **CONFIG_BOTON
    ).place(x=600, y=500)