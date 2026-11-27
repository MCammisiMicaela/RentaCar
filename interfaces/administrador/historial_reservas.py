import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from recursos.estilos import *
from servicios.gestion_reservas import cargar_reservas
from servicios.gestion_autos import cargar_autos
from servicios.persistencia import cargar_json, guardar_json
import os

RUTA_ICONOS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "recursos", "iconos"))
IMAGEN_POR_DEFECTO = os.path.join(RUTA_ICONOS, "auto_generico.png")

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


def mostrar_historial_admin(usuario_actual, ventana):
    from interfaces.administrador.menu_admin import mostrar_menu_admin

    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.title("Historial de reservas")
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

    tk.Label(ventana, text="Historial de reservas", **CONFIG_LABEL_TITULO).place(x=30, y=140)

    # Buscador
    tk.Label(ventana, text="Buscar por patente o usuario:", **CONFIG_LABEL_FORMULARIO).place(x=30, y=190)
    entrada_busqueda = tk.Entry(ventana, width=30)
    entrada_busqueda.bind("<KeyRelease>", lambda e: mostrar_reservas(filtro=entrada_busqueda.get().strip()))
    entrada_busqueda.place(x=250, y=190)

    # Canvas y scroll
    contenedor_canvas = tk.Canvas(ventana, bg=COLOR_BOTON)
    contenedor_canvas.place(x=30, y=230, width=720, height=300)
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=contenedor_canvas.yview)
    scrollbar.place(x=750, y=230, height=300)

    marco_historial = tk.Frame(contenedor_canvas, bg=COLOR_BOTON)
    contenedor_canvas.create_window((0, 0), window=marco_historial, anchor="nw")
    contenedor_canvas.configure(yscrollcommand=scrollbar.set)

    marco_historial.bind("<Configure>", lambda e: contenedor_canvas.configure(scrollregion=contenedor_canvas.bbox("all")))
    contenedor_canvas.bind_all("<MouseWheel>", lambda e: contenedor_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def mostrar_reservas(filtro=""):
        for widget in marco_historial.winfo_children():
            widget.destroy()

        reservas = cargar_reservas()
        autos = cargar_autos()

        historial = sorted(
            [r for r in reservas if all(k in r for k in ("id_reserva", "patente", "usuario", "desde", "hasta", "estado"))],
            key=lambda r: r.get("desde", ""),
            reverse=True
        )

        if not historial:
            tk.Label(marco_historial, text="No hay reservas para mostrar.", font=("Segoe UI", 10, "italic"), fg=COLOR_ERROR, bg=COLOR_BOTON).grid(row=0, column=0, padx=10, pady=10)
            return

        for i, reserva in enumerate(historial):
            auto = next((a for a in autos if a.patente.strip().upper() == reserva["patente"].strip().upper()), None)
            # Filtrado por patente o usuario
            if filtro and not (
                (auto and filtro.lower() in auto.patente.lower()) or
                (filtro.lower() in reserva["usuario"].lower())
            ):
                continue

            frame_reserva = tk.Frame(marco_historial, bg=COLOR_BOTON, bd=2, relief="groove", width=740, height=100)
            frame_reserva.grid_propagate(False)
            frame_reserva.grid(row=i, column=0, padx=10, pady=8, sticky="ew")

            # Configurar columnas para buena alineación
            frame_reserva.columnconfigure(0, minsize=110)
            frame_reserva.columnconfigure(1, minsize=170)
            frame_reserva.columnconfigure(2, minsize=160)
            frame_reserva.columnconfigure(3, minsize=180)

            if auto:
                fecha_desde = datetime.strptime(reserva["desde"], "%Y-%m-%d").date()
                fecha_hasta = datetime.strptime(reserva["hasta"], "%Y-%m-%d").date()
                dias = (fecha_hasta - fecha_desde).days + 1
                precio_total = auto.precio_por_dia * dias

                # Columna 0: Imagen del auto
                img_tk = cargar_imagen_auto(auto.foto)
                if img_tk:
                    lbl_img = tk.Label(frame_reserva, image=img_tk, bg=COLOR_BOTON)
                    lbl_img.image = img_tk
                    lbl_img.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="ns")
                else:
                    tk.Label(frame_reserva, text="Sin imagen", fg="red", bg=COLOR_BOTON).grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="ns")

                # Columna 1: Datos del auto
                tk.Label(frame_reserva, text=f"ID: {reserva['id_reserva']}", font=("Segoe UI", 10, "bold"), bg=COLOR_BOTON).grid(row=0, column=1, sticky="w", padx=10, pady=(8,2))
                tk.Label(frame_reserva, text=f"{auto.marca} {auto.modelo}", font=("Segoe UI", 10), bg=COLOR_BOTON).grid(row=1, column=1, sticky="w", padx=10, pady=2)
                tk.Label(frame_reserva, text=f"Patente: {auto.patente}", font=("Segoe UI", 9), bg=COLOR_BOTON).grid(row=2, column=1, sticky="w", padx=10, pady=(2,8))

                # Columna 2: Fechas y total
                tk.Label(frame_reserva, text=f"Desde: {reserva['desde']}", font=("Segoe UI", 9), bg=COLOR_BOTON).grid(row=0, column=2, sticky="w", padx=10, pady=(8,2))
                tk.Label(frame_reserva, text=f"Hasta: {reserva['hasta']}", font=("Segoe UI", 9), bg=COLOR_BOTON).grid(row=1, column=2, sticky="w", padx=10, pady=2)
                tk.Label(frame_reserva, text=f"Total: ${precio_total}", font=("Segoe UI", 10, "bold"), bg=COLOR_BOTON).grid(row=2, column=2, sticky="w", padx=10, pady=(2,8))

                # Columna 3: Usuario, estado y puntaje
                tk.Label(frame_reserva, text=f"Usuario: {reserva['usuario']}", font=("Segoe UI", 10, "bold"), bg=COLOR_BOTON).grid(row=0, column=3, sticky="w", padx=10, pady=(8,2))

                estado = reserva["estado"].lower()
                color_estado = {
                    "activa": COLOR_FONDO,
                    "finalizada": COLOR_EXITO,
                    "cancelada": COLOR_ERROR
                }.get(estado, "black")

                tk.Label(frame_reserva, text=f"Estado: {estado.capitalize()}", font=("Segoe UI", 10, "bold"), fg=color_estado, bg=COLOR_BOTON).grid(row=1, column=3, sticky="w", padx=10, pady=2)

                if estado == "finalizada":
                    if "puntaje" in reserva and isinstance(reserva["puntaje"], (int, float)):
                        estrellas = "⭐" * int(reserva["puntaje"])
                        texto_puntaje = f"Puntaje: {estrellas} ({reserva['puntaje']}/5)"
                        tk.Label(frame_reserva, text=texto_puntaje, font=("Segoe UI", 9), fg=COLOR_PUNTUACION, bg=COLOR_BOTON).grid(row=2, column=3, sticky="w", padx=10, pady=(2,8))
                    else:
                        tk.Label(frame_reserva, text="Sin puntuación registrada", font=("Segoe UI", 9, "italic"), fg="gray", bg=COLOR_BOTON).grid(row=2, column=3, sticky="w", padx=10, pady=(2,8))
            else:
                mensaje = (
                    f"Reserva {reserva['id_reserva']} | Patente {reserva['patente']} no encontrada\n"
                    f"Usuario: {reserva['usuario']} | Desde: {reserva['desde']} Hasta: {reserva['hasta']} | Estado: {reserva['estado']}"
                )
                tk.Label(frame_reserva, text=mensaje, fg="red", font=("Segoe UI", 9), justify="left", wraplength=600, bg=COLOR_BOTON).grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")

        marco_historial.update_idletasks()
        contenedor_canvas.configure(scrollregion=contenedor_canvas.bbox("all"))

    ventana.after(100, lambda: mostrar_reservas(""))

    def volver_al_menu_admin():
        mostrar_menu_admin(usuario_actual, ventana)

    tk.Button(ventana, text="Volver al menú", command=volver_al_menu_admin, **CONFIG_BOTON_FORMULARIO).place(x=600, y=550)