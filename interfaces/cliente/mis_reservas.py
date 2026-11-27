import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
from recursos.estilos import *
from servicios.gestion_autos import cargar_autos
from servicios.gestion_reservas import cargar_reservas, cancelar_reserva as cancelar_reserva_servicio
from servicios.persistencia import cargar_json, guardar_json
from interfaces.cliente.puntuar_auto import abrir_ventana_puntuar
import os

# Ruta fija para las imágenes
RUTA_ICONOS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "recursos", "iconos"))
IMAGEN_POR_DEFECTO = os.path.join(RUTA_ICONOS, "auto_generico.png")

# Carga una imagen del auto o una genérica si no existe
def cargar_imagen_auto(nombre_archivo, ancho=100, alto=70):
    try:
        ruta_imagen = os.path.join(RUTA_ICONOS, nombre_archivo)
        if not os.path.isfile(ruta_imagen):
            ruta_imagen = IMAGEN_POR_DEFECTO
        imagen = Image.open(ruta_imagen).resize((ancho, alto))
        return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print("Error al cargar imagen:", e)
        return None


# Muestra el historial de reservas del cliente
def mostrar_mis_reservas(usuario_actual, ventana):
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.title("Mis reservas")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    # Fondo visual
    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize(TAMANIO_FONDO)
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        ventana.fondo_img = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar fondo:", e)

    tk.Label(ventana, text="Historial de reservas", **CONFIG_LABEL_TITULO).place(x=50, y=140)

    # Buscador
    tk.Label(ventana, text="Buscar por patente:", **CONFIG_LABEL_FORMULARIO).place(x=30, y=190)
    entrada_busqueda = tk.Entry(ventana, width=30)
    entrada_busqueda.bind("<KeyRelease>", lambda e: mostrar_reservas(filtro_patente=entrada_busqueda.get().strip()))
    entrada_busqueda.place(x=200, y=190)

    # Scroll con canvas
    canvas = tk.Canvas(ventana, bg=COLOR_BOTON)
    canvas.place(x=30, y=230, width=720, height=300)
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    scrollbar.place(x=750, y=230, height=300)

    marco_historial = tk.Frame(canvas, bg=COLOR_BOTON)
    canvas.create_window((0, 0), window=marco_historial, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    marco_historial.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def mostrar_reservas(filtro_patente=""):
        for widget in marco_historial.winfo_children():
            widget.destroy()

        reservas = cargar_reservas()
        autos = cargar_autos()

        historial = sorted(
            [r for r in reservas if r["usuario"] == usuario_actual.usuario],
            key=lambda r: r["desde"],
            reverse=True
        )

        if not historial:
            tk.Label(marco_historial, text="No hay reservas para mostrar.", font=("Segoe UI", 10, "italic"), fg=COLOR_ERROR, bg=COLOR_BOTON).grid(row=0, column=0, padx=10, pady=10)
            return

        for i, reserva in enumerate(historial):
            auto = next((a for a in autos if a.patente == reserva["patente"]), None)
            if not auto:
                continue

            if filtro_patente and auto and filtro_patente.lower() not in auto.patente.lower():
                continue


            frame = tk.Frame(marco_historial, bg=COLOR_BOTON, bd=2, relief="groove", width=740, height=100)
            frame.grid_propagate(False)
            frame.grid(row=i, column=0, padx=10, pady=8, sticky="ew")

            # Alineación de columnas como en gestión de autos
            frame.columnconfigure(0, minsize=110)  # Imagen
            frame.columnconfigure(1, minsize=170)  # Datos del auto
            frame.columnconfigure(2, minsize=160)  # Fechas y total
            frame.columnconfigure(3, minsize=180)  # Estado y acciones

            # Imagen
            img_tk = cargar_imagen_auto(auto.foto)
            if img_tk:
                lbl_img = tk.Label(frame, image=img_tk, bg=COLOR_BOTON)
                lbl_img.image = img_tk
            else:
                lbl_img = tk.Label(frame, text="Sin imagen", fg="red", bg=COLOR_BOTON)
            lbl_img.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="ns")

            # Datos del auto
            tk.Label(frame, text=f"Patente: {auto.patente}", font=("Segoe UI", 11, "bold"), bg=COLOR_BOTON).grid(row=0, column=1, sticky="w", padx=20, pady=(8,2))
            tk.Label(frame, text=f"{auto.marca} {auto.modelo}", font=("Segoe UI", 10), bg=COLOR_BOTON).grid(row=1, column=1, sticky="w", padx=20, pady=2)
            tk.Label(frame, text=f"Transmisión: {auto.transmision}", font=("Segoe UI", 9), bg=COLOR_BOTON).grid(row=2, column=1, sticky="w", padx=20, pady=(2,8))

            # Fechas y total
            fecha_desde = datetime.strptime(reserva["desde"], "%Y-%m-%d").date()
            fecha_hasta = datetime.strptime(reserva["hasta"], "%Y-%m-%d").date()
            dias = (fecha_hasta - fecha_desde).days + 1
            precio_total = auto.precio_por_dia * dias
            tk.Label(frame, text=f"Desde: {reserva['desde']}", font=("Segoe UI", 9), bg=COLOR_BOTON).grid(row=0, column=2, sticky="w", padx=20, pady=(8,2))
            tk.Label(frame, text=f"Hasta: {reserva['hasta']}", font=("Segoe UI", 9), bg=COLOR_BOTON).grid(row=1, column=2, sticky="w", padx=20, pady=2)
            tk.Label(frame, text=f"Total: ${precio_total}", font=("Segoe UI", 10, "bold"), bg=COLOR_BOTON).grid(row=2, column=2, sticky="w", padx=20, pady=(2,8))

            # Estado y acciones
            estado = reserva["estado"]
            color_estado = {
                "activa": COLOR_FONDO,
                "finalizada": COLOR_EXITO,
                "cancelada": COLOR_ERROR
            }.get(estado, "black")
            tk.Label(frame, text=f"Estado: {estado.capitalize()}", font=("Segoe UI", 11, "bold"), fg=color_estado, bg=COLOR_BOTON).grid(row=0, column=3, sticky="w", padx=20, pady=(8,2))

            if estado == "activa":
                tk.Button(frame, text="Cancelar reserva", command=lambda r=reserva: cancelar_reserva(r, ventana, usuario_actual), **CONFIG_BOTON_INFO).grid(row=1, column=3, sticky="w", padx=20, pady=2)

            if estado == "finalizada":
                if isinstance(reserva.get("puntaje"), (int, float)):
                    estrellas = "⭐" * int(reserva["puntaje"])
                    tk.Label(frame, text=f"Puntaje: {estrellas}", font=("Segoe UI", 10), fg=COLOR_PUNTUACION, bg=COLOR_BOTON).grid(row=2, column=3, sticky="w", padx=20, pady=(2,8))
                else:
                    tk.Button(frame, text="Puntuar", command=lambda r=reserva: abrir_ventana_puntuar(r, usuario_actual, ventana), **CONFIG_BOTON_INFO).grid(row=2, column=3, sticky="w", padx=20, pady=(2,8))

        marco_historial.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    ventana.after(100, lambda: mostrar_reservas(""))

    tk.Button(ventana, text="Volver al menú", command=lambda: volver_al_menu_cliente(usuario_actual, ventana), **CONFIG_BOTON_FORMULARIO).place(x=650, y=550)

# Cancela una reserva activa y actualiza el historial
def cancelar_reserva(reserva, ventana, usuario_actual):
    exito, mensaje = cancelar_reserva_servicio(
        reserva["id_reserva"], usuario=usuario_actual.usuario
    )
    if exito:
        messagebox.showinfo("Reserva cancelada", mensaje)
    else:
        messagebox.showerror("No se pudo cancelar", mensaje)
    mostrar_mis_reservas(usuario_actual, ventana)

# Vuelve al menú principal del cliente
def volver_al_menu_cliente(usuario_actual, ventana):
    from interfaces.cliente.menu_cliente import mostrar_menu_cliente
    mostrar_menu_cliente(usuario_actual, ventana)
