import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from recursos.estilos import *
from interfaces.comunes.registro_usuario import mostrar_registro_usuario
import json, os

RUTA_USUARIOS = os.path.join("datos", "usuarios.json")

def mostrar_gestion_administradores(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.deiconify()
    ventana.title("Gestión de administradores")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    # Fondo
    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize(TAMANIO_FONDO)
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        ventana.fondo_img = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar fondo:", e)

    tk.Label(ventana, text="Administradores registrados:", **CONFIG_LABEL_TITULO).place(x=50, y=140)

    columnas = ("usuario", "nombre", "apellido", "celular", "fecha_nacimiento")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)
    tabla.place(x=50, y=200)

    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=120)

    mensaje_label = tk.Label(ventana, text="", **CONFIG_MENSAJE)
    mensaje_label.place(x=50, y=440)

    info_label = tk.Label(ventana, text="", justify="left", **CONFIG_MENSAJE)
    info_label.place(x=600, y=200)

    def cargar_lista_administradores():
        tabla.delete(*tabla.get_children())
        try:
            with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
                usuarios = json.load(archivo)
        except:
            usuarios = {}

        for usuario, datos in usuarios.items():
            if datos.get("tipo") == "admin":
                fila = (
                    usuario,
                    datos.get("nombre", "-"),
                    datos.get("apellido", "-"),
                    datos.get("celular", "-"),
                    datos.get("fecha_nacimiento", "-")
                )
                tabla.insert("", tk.END, values=fila)

        info_label.config(text="")  # limpiar info al recargar

    def eliminar_admin():
        seleccionado = tabla.focus()
        if not seleccionado:
            mensaje_label.config(text="Seleccioná un administrador para eliminar.", fg=COLOR_ERROR)
            return

        usuario = tabla.item(seleccionado)["values"][0]
        if usuario == "admin_general":
            mensaje_label.config(text="No se puede eliminar al administrador general.", fg=COLOR_ERROR)
            return

        try:
            with open(RUTA_USUARIOS, "r", encoding="utf-8") as archivo:
                usuarios = json.load(archivo)
        except:
            usuarios = {}

        if usuario in usuarios:
            del usuarios[usuario]
            with open(RUTA_USUARIOS, "w", encoding="utf-8") as archivo:
                json.dump(usuarios, archivo, indent=4)

            cargar_lista_administradores()
            mensaje_label.config(text=f"Administrador '{usuario}' eliminado.", fg=COLOR_EXITO)

    def agregar_admin():
        mostrar_registro_usuario(
            tipo_usuario="admin",
            titulo="Crear nuevo administrador",
            mensaje_exito="Administrador creado con éxito.",
            ventana=ventana  # se espera que mostrar_registro_usuario lo acepte
        )

    def volver_al_menu_admin():
        from interfaces.administrador.menu_admin import mostrar_menu_admin
        mostrar_menu_admin("admin_general", ventana)
    tk.Button(ventana, text="Eliminar", command=eliminar_admin, **CONFIG_BOTON_FORMULARIO).place(x=50, y=500)
    tk.Button(ventana, text="Agregar", command=agregar_admin, **CONFIG_BOTON_FORMULARIO).place(x=600, y=140)
    tk.Button(ventana, text="Volver al menú", command=volver_al_menu_admin, **CONFIG_BOTON_FORMULARIO).place(x=600, y=500)

    cargar_lista_administradores()