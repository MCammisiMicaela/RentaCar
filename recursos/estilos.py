import os

# Tipografías
TIPO_LETRA = ("Segoe UI", 11)
TIPO_TITULO = ("Segoe UI", 16, "bold")
TIPO_TITULO_GRANDE = ("Segoe UI", 24, "bold")

# Colores
COLOR_FONDO = "#003F4F"
COLOR_TEXTO = "#F2F2F2"
COLOR_TEXTO_BOTON = "#003F4F"
COLOR_BOTON = "#F2F2F2"
COLOR_HOVER_BOTON_CLARO = "#D1DAC3"
COLOR_ERROR = "#C0392B"
COLOR_EXITO = "#4CAF50"
COLOR_PUNTUACION = "#9E8600"

# Rutas de imagen
RUTA_FONDO = os.path.join("recursos", "fondo.png")
RUTA_FONDO_LIMPIO = os.path.join("recursos", "fondo_limpio.png")

# Dimensiones generales
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
TAMANIO_FONDO = (ANCHO_VENTANA, ALTO_VENTANA)

# Entradas de texto
CONFIG_ENTRY = {
    "width": 30,
    "bg": COLOR_TEXTO,
    "fg": COLOR_FONDO,
    "font": TIPO_LETRA,
    "insertbackground": COLOR_FONDO
}

# Calendarios
CONFIG_FECHA = {
    "width": 27,
    "background": COLOR_TEXTO,
    "foreground": COLOR_FONDO,
    "borderwidth": 2,
    "date_pattern": "dd/mm/yyyy",
    "font": TIPO_LETRA,
    "insertbackground": COLOR_FONDO
}

CONFIG_ENTRY_FECHA = {
    "width": 20,
    "date_pattern": "dd/mm/yyyy",
    "font": TIPO_LETRA,
    "foreground": COLOR_FONDO,  # texto dentro del campo
    "background": "white",      # fondo del campo (no del calendario)
    "state": "readonly"         # evita edición manual si querés
}

# Calendario visual
CONFIG_CALENDARIO = {
    "selectmode": "day",
    "date_pattern": "yyyy-mm-dd",
    "showweeknumbers": False,
    "background": COLOR_FONDO,
    "foreground": COLOR_TEXTO,
    "headersbackground": COLOR_FONDO,
    "headersforeground": COLOR_TEXTO,
    "selectbackground": "#66A6B6",  # color de selección
    "selectforeground": COLOR_TEXTO_BOTON,
    "bordercolor": COLOR_BOTON,
    "normalbackground": COLOR_BOTON,
    "normalforeground": COLOR_TEXTO_BOTON
}

# Etiquetas
CONFIG_LABEL_FORMULARIO = {
    "font": TIPO_LETRA,
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO
}

CONFIG_LABEL_SECCION = {
    "font": ("Segoe UI", 14, "bold"),
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO
}

CONFIG_LABEL_FILTRO = {
    "font": TIPO_LETRA,
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO
}

CONFIG_LABEL_TITULO = {
    "font": TIPO_TITULO,
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO
}

CONFIG_LABEL_TITULO_GRANDE = {
    "font": TIPO_TITULO_GRANDE,
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO
}

# Mensajes dinámicos
CONFIG_MENSAJE = {
    "font": TIPO_LETRA,
    "bg": COLOR_FONDO
}

# Botones
CONFIG_BOTON_FORMULARIO = {
    "font": TIPO_LETRA,
    "bg": COLOR_BOTON,
    "fg": COLOR_TEXTO_BOTON,
    "activebackground": COLOR_HOVER_BOTON_CLARO,
    "width": 17,
    "borderwidth": 0
}

CONFIG_BOTON_MINI = {
    "font": ("Segoe UI", 10),
    "bg": COLOR_BOTON,
    "fg": COLOR_TEXTO_BOTON,
    "activebackground": COLOR_HOVER_BOTON_CLARO,
    "width": 15,
    "borderwidth": 0
}

CONFIG_BOTON_INFO = {
    "font": ("Segoe UI", 10),
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO,
    "activebackground": "#0386A7",
    "width": 15,
    "borderwidth": 0
}

CONFIG_BOTON = {
    "font": TIPO_LETRA,
    "bg": COLOR_BOTON,
    "fg": COLOR_FONDO,
    "activebackground": COLOR_HOVER_BOTON_CLARO,
    "width": 20,
    "height": 2,
    "borderwidth": 0
}
