import tkinter as tk
from PIL import Image, ImageTk
from recursos.estilos import *
from interfaces.administrador.gestion_administradores import mostrar_gestion_administradores
from interfaces.administrador.gestionar_clientes import mostrar_gestion_clientes
from interfaces.comunes.mi_cuenta import mostrar_mi_cuenta

def mostrar_menu_admin(usuario_actual, ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.deiconify()
    ventana.title("RentaCar - Sistema administrativo")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize(TAMANIO_FONDO)
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar fondo:", e)

    # Encabezado
    tk.Label(ventana, text="Sistema administrativo de gestión", **CONFIG_LABEL_TITULO).place(x=30, y=140)
    
    # Botones de gestión
    botones_izquierda = [
        ("Clientes", lambda: mostrar_gestion_clientes(usuario_actual, ventana)),
        ("Historial de reservas", lambda: print("Ir a Historial")),
        ("Gestión de autos", lambda: print("Ir a Gestión de autos")),
        ("Agregar auto", lambda: print("Ir a Agregar auto"))
    ]

    if usuario_actual.usuario == "admin_general":
        botones_izquierda.insert(1, ("Administradores", lambda: mostrar_gestion_administradores(usuario_actual, ventana)))


    for i, (texto, comando) in enumerate(botones_izquierda):
        tk.Button(ventana, text=texto, command=comando, **CONFIG_BOTON).place(x=50, y=220 + i * 60)
    
    def cerrar_sesion():
        from interfaces.comunes.login import mostrar_login
        mostrar_login(ventana)

    # Botones de cuenta personal
    tk.Button(ventana, text="Mi cuenta", command=lambda: mostrar_mi_cuenta(usuario_actual, ventana), **CONFIG_BOTON_FORMULARIO).place(x=600, y=200)
    tk.Button(ventana,text="Cerrar sesión", command=cerrar_sesion, **CONFIG_BOTON_FORMULARIO).place(x=600, y=260)