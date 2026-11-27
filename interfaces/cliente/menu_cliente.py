
import tkinter as tk
from datetime import date, timedelta

from PIL import Image, ImageTk
from tkcalendar import Calendar

from recursos.estilos import *
from interfaces.comunes.mi_cuenta import mostrar_mi_cuenta
from interfaces.cliente.buscar_auto import mostrar_buscar_autos
from interfaces.cliente.mis_reservas import mostrar_mis_reservas


def mostrar_menu_cliente(usuario_actual, ventana):
    """
    Muestra el menú principal del cliente.
    Permite seleccionar fechas y buscar vehículos disponibles.
    """

    # Limpiar la ventana anterior.
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.deiconify()
    ventana.title("RentaCar - Alquiler de autos")
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
        text="Alquiler de autos",
        **CONFIG_LABEL_TITULO_GRANDE
    ).place(x=30, y=140)

    tk.Label(
        ventana,
        text="Ubi: Terminal de colectivos, Esperanza",
        **CONFIG_LABEL_FORMULARIO
    ).place(x=30, y=200)

    # Cerrar sesión.
    def cerrar_sesion():
        from interfaces.comunes.login import mostrar_login
        mostrar_login(ventana)

    # Botones de navegación.
    botones_derecha = [
        (
            "Mi cuenta",
            200,
            lambda: mostrar_mi_cuenta(usuario_actual, ventana)
        ),
        (
            "Mis reservas",
            260,
            lambda: mostrar_mis_reservas(usuario_actual, ventana)
        ),
        (
            "Cerrar sesión",
            320,
            cerrar_sesion
        )
    ]

    for texto, y, comando in botones_derecha:
        tk.Button(
            ventana,
            text=texto,
            command=comando,
            **CONFIG_BOTON_FORMULARIO
        ).place(x=600, y=y)

    # Selección de fechas.
    tk.Label(
        ventana,
        text="Seleccioná las fechas de entrega y devolución:",
        **CONFIG_LABEL_TITULO
    ).place(x=30, y=300)

    hoy = date.today()

    calendario = Calendar(
        ventana,
        selectmode="day",
        date_pattern="yyyy-mm-dd",
        mindate=hoy,
        font=TIPO_LETRA,
        background=COLOR_FONDO,
        foreground=COLOR_TEXTO,
        headersbackground=COLOR_FONDO,
        headersforeground=COLOR_TEXTO,
        selectbackground="#66A6B6",
        selectforeground="black"
    )

    calendario.place(x=40, y=350)

    # Color del rango de fechas seleccionado.
    calendario.tag_config(
        "rango",
        background="#66A6B6",
        foreground="black"
    )

    # Mensajes de selección.
    etiqueta_estado = tk.Label(
        ventana,
        text="Seleccioná primero la entrega y luego la devolución.",
        **CONFIG_LABEL_FORMULARIO
    )
    etiqueta_estado.place(x=40, y=550)

    # Estado de las fechas.
    fecha_entrega = None
    fecha_devolucion = None
    seleccionando_entrega = True
    eventos_rango = []

    def limpiar_rango():
        """Elimina los indicadores de fechas anteriores."""
        for evento_id in eventos_rango:
            calendario.calevent_remove(evento_id)

        eventos_rango.clear()

    def manejar_seleccion(evento=None):
        """
        Registra la fecha de entrega y la de devolución.
        Evita seleccionar fechas pasadas o rangos inválidos.
        """
        nonlocal fecha_entrega
        nonlocal fecha_devolucion
        nonlocal seleccionando_entrega

        seleccion = calendario.selection_get()

        if seleccion < hoy:
            etiqueta_estado.config(
                text="No se pueden seleccionar fechas pasadas.",
                fg=COLOR_ERROR
            )
            return

        # Primera fecha: entrega del vehículo.
        if seleccionando_entrega:
            limpiar_rango()

            fecha_entrega = seleccion
            fecha_devolucion = None
            seleccionando_entrega = False

            etiqueta_estado.config(
                text=f"Entrega: {fecha_entrega}. Seleccioná la devolución.",
                fg=COLOR_TEXTO
            )
            return

        # Segunda fecha: devolución del vehículo.
        if seleccion < fecha_entrega:
            fecha_entrega = None
            fecha_devolucion = None
            seleccionando_entrega = True

            etiqueta_estado.config(
                text="La devolución no puede ser anterior a la entrega.",
                fg=COLOR_ERROR
            )
            return

        fecha_devolucion = seleccion

        # Marcar el rango seleccionado.
        dia = fecha_entrega

        while dia <= fecha_devolucion:
            evento_id = calendario.calevent_create(
                dia,
                "Seleccionado",
                "rango"
            )

            eventos_rango.append(evento_id)
            dia += timedelta(days=1)

        etiqueta_estado.config(
            text=f"Entrega: {fecha_entrega} | Devolución: {fecha_devolucion}",
            fg=COLOR_EXITO
        )

        # La próxima selección inicia un rango nuevo.
        seleccionando_entrega = True

    calendario.bind(
        "<<CalendarSelected>>",
        manejar_seleccion
    )

    # Buscar vehículos disponibles.
    def buscar():
        if fecha_entrega is None or fecha_devolucion is None:
            etiqueta_estado.config(
                text="Seleccioná ambas fechas antes de continuar.",
                fg=COLOR_ERROR
            )
            return

        mostrar_buscar_autos(
            usuario_actual,
            ventana,
            fecha_entrega,
            fecha_devolucion
        )

    tk.Button(
        ventana,
        text="Buscar",
        command=buscar,
        **CONFIG_BOTON_FORMULARIO
    ).place(x=600, y=500)
