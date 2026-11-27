
import tkinter as tk
from PIL import Image, ImageTk

from recursos.estilos import *

from interfaces.administrador.gestion_administradores import mostrar_gestion_administradores
from interfaces.administrador.gestionar_clientes import mostrar_gestion_clientes
from interfaces.administrador.gestionar_autos import mostrar_gestion_autos
from interfaces.administrador.historial_reservas import mostrar_historial_admin
from interfaces.comunes.mi_cuenta import mostrar_mi_cuenta


def mostrar_menu_admin(usuario_actual, ventana):
    """
    Muestra el menú principal del administrador y permite
    acceder a las funcionalidades de gestión del sistema.
    """

    # Limpiar la ventana anterior.
    for widget in ventana.winfo_children():
        widget.destroy()

    # Configuración de la ventana.
    ventana.deiconify()
    ventana.title("RentaCar - Sistema administrativo")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    # Imagen de fondo.
    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize(TAMANIO_FONDO)
        fondo_img = ImageTk.PhotoImage(fondo)

        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

    except Exception as error:
        print("Error al cargar el fondo:", error)

    # Encabezado.
    tk.Label(
        ventana,
        text="Sistema administrativo de gestión",
        **CONFIG_LABEL_TITULO
    ).place(x=30, y=140)

    # Funcionalidades disponibles para administradores.
    botones_izquierda = [
        (
            "Clientes",
            lambda: mostrar_gestion_clientes(usuario_actual, ventana)
        ),
        (
            "Historial de reservas",
            lambda: mostrar_historial_admin(usuario_actual, ventana)
        ),
        (
            "Gestión de autos",
            lambda: mostrar_gestion_autos(usuario_actual, ventana)
        )
    ]

    # Solo el administrador general puede gestionar administradores.
    if usuario_actual.usuario == "admin_general":
        botones_izquierda.insert(
            1,
            (
                "Administradores",
                lambda: mostrar_gestion_administradores(
                    usuario_actual, ventana
                )
            )
        )

    # Crear botones de navegación.
    for i, (texto, comando) in enumerate(botones_izquierda):
        tk.Button(
            ventana,
            text=texto,
            command=comando,
            **CONFIG_BOTON
        ).place(x=50, y=220 + i * 60)

    # Gestión de la cuenta personal.
    tk.Button(
        ventana,
        text="Mi cuenta",
        command=lambda: mostrar_mi_cuenta(usuario_actual, ventana),
        **CONFIG_BOTON_FORMULARIO
    ).place(x=600, y=200)

    # Cerrar sesión.
    def cerrar_sesion():
        from interfaces.comunes.login import mostrar_login
        mostrar_login(ventana)

    tk.Button(
        ventana,
        text="Cerrar sesión",
        command=cerrar_sesion,
        **CONFIG_BOTON_FORMULARIO
    ).place(x=600, y=260)
