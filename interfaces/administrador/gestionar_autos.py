from servicios.gestion_reservas import cargar_reservas
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from recursos.estilos import *
from servicios.gestion_autos import cargar_autos, guardar_autos, buscar_auto_por_patente
from interfaces.administrador.formulario_auto import mostrar_formulario_auto
from servicios.persistencia import cargar_json
import os

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

# Muestra la interfaz de gestión de autos para el administrador
def mostrar_gestion_autos(usuario_actual, ventana):
    # Limpia la ventana actual
    for widget in ventana.winfo_children():
        widget.destroy()

    # Configura la ventana
    ventana.deiconify()
    ventana.title("Gestión de autos")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    # Carga el fondo visual
    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize(TAMANIO_FONDO)
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        ventana.fondo_img = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar fondo:", e)

    # Título de sección
    tk.Label(ventana, text="Autos registrados", **CONFIG_LABEL_TITULO).place(x=50, y=140)

    # Área con scroll para mostrar autos
    canvas = tk.Canvas(ventana, bg=COLOR_BOTON)
    canvas.place(x=10, y=240, width=760, height=280)
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    scrollbar.place(x=770, y=240, height=280)
    marco_autos = tk.Frame(canvas, bg=COLOR_BOTON)
    canvas.create_window((0, 0), window=marco_autos, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    marco_autos.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # Mensaje dinámico para mostrar acciones
    mensaje_accion = tk.Label(ventana, text="", **CONFIG_MENSAJE)
    mensaje_accion.place(x=50, y=520)

    # Campo de búsqueda por patente
    tk.Label(ventana, text="Buscar por patente:", **CONFIG_LABEL_FORMULARIO).place(x=50, y=200)
    entrada_busqueda = tk.Entry(ventana, width=20, font=TIPO_LETRA)
    entrada_busqueda.bind("<KeyRelease>", lambda e: cargar_lista_autos(filtro_patente=entrada_busqueda.get().strip()))
    entrada_busqueda.place(x=200, y=200)

    # Carga y muestra la lista de autos, filtrando si se indica
    def cargar_lista_autos(filtro_patente=""):
        for widget in marco_autos.winfo_children():
            widget.destroy()

        autos = cargar_autos()
        autos_filtrados = [a for a in autos if filtro_patente.lower() in a.patente.lower()] if filtro_patente else autos

        if not autos_filtrados:
            tk.Label(marco_autos, text="No se encontraron autos.", font=("Segoe UI", 10), fg=COLOR_ERROR, bg=COLOR_BOTON).grid(row=0, column=0, padx=10, pady=10)
            return

        reservas = cargar_reservas()

        for i, auto in enumerate(autos_filtrados):
            frame = tk.Frame(marco_autos, bg=COLOR_BOTON, bd=2, relief="groove", width=740, height=100)
            frame.grid_propagate(False)
            frame.grid(row=i, column=0, padx=10, pady=8, sticky="ew")
            frame.columnconfigure(4, minsize=120)  # Reservar espacio para botones

            # Imagen del auto
            img_tk = cargar_imagen_auto(auto.foto)
            if img_tk:
                lbl_img = tk.Label(frame, image=img_tk, bg=COLOR_BOTON)
                lbl_img.image = img_tk
                lbl_img.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="ns")
            else:
                tk.Label(frame, text="Sin imagen", fg="red", bg=COLOR_BOTON).grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="ns")

            # Datos principales: patente, marca, modelo, precio
            tk.Label(frame, text=f"Patente: {auto.patente}", font=("Segoe UI", 11, "bold"), bg=COLOR_BOTON).grid(row=0, column=1, sticky="w", padx=20, pady=(8,2))
            tk.Label(frame, text=f"{auto.marca} {auto.modelo}", font=("Segoe UI", 10), bg=COLOR_BOTON).grid(row=1, column=1, sticky="w", padx=20, pady=2)
            tk.Label(frame, text=f"Precio por día: ${auto.precio_por_dia}", font=("Segoe UI", 9), bg=COLOR_BOTON).grid(row=2, column=1, sticky="w", padx=20, pady=2)

            # Estado del auto (bloqueado o disponible)
            estado = "Bloqueado" if auto.bloqueado else "Disponible"
            color_estado = COLOR_ERROR if auto.bloqueado else COLOR_EXITO
            tk.Label(frame, text=f"Estado: {estado}", font=("Segoe UI", 11, "bold"), fg=color_estado, bg=COLOR_BOTON).grid(row=0, column=2, sticky="w", padx=20, pady=(8,2))

            # Puntuación promedio del auto
            puntuaciones = [
                r.get("puntaje") for r in reservas
                if r.get("patente", "").strip().upper() == auto.patente.strip().upper()
                and isinstance(r.get("puntaje"), (int, float))
            ]
            if puntuaciones:
                promedio = round(sum(puntuaciones) / len(puntuaciones), 1)
                estrellas = "⭐" * int(round(promedio))
                texto_puntaje = f"Puntaje: {estrellas} ({promedio}/5) | {len(puntuaciones)} opiniones"
            else:
                texto_puntaje = "Sin puntuación registrada"

            tk.Label(frame, text=texto_puntaje, font=("Segoe UI", 9), fg=COLOR_PUNTUACION if puntuaciones else "gray", bg=COLOR_BOTON).grid(row=2, column=2, sticky="w", padx=20, pady=(2,8))

            # Botón para bloquear o desbloquear el auto
            def actualizar_estado_bloqueo(a, bloquear):
                a.bloqueado = bloquear
                guardar_autos(autos)
                cargar_lista_autos()
                estado_txt = "bloqueado" if bloquear else "desbloqueado"
                mensaje_accion.config(text=f"Auto {a.patente} {estado_txt}.", fg=COLOR_EXITO if not bloquear else COLOR_ERROR)

            if auto.bloqueado:
                tk.Button(frame, text="Desbloquear", command=lambda a=auto: actualizar_estado_bloqueo(a, False), **CONFIG_BOTON_INFO).grid(row=1, column=2, sticky="w", padx=20, pady=2)
            else:
                tk.Button(frame, text="Bloquear", command=lambda a=auto: actualizar_estado_bloqueo(a, True), **CONFIG_BOTON_INFO).grid(row=1, column=2, sticky="w", padx=20, pady=2)

            # Verifica si el auto tiene reservas antes de permitir eliminarlo
            tiene_reservas = any(
                r.get("patente", "").strip().upper() == auto.patente.strip().upper()
                for r in reservas
            )

            def eliminar_auto_individual(a):
                if tiene_reservas:
                    messagebox.showerror("Error", f"No se puede eliminar el auto {a.patente} porque tiene reservas asociadas.")
                    return
                autos_actualizados = [x for x in autos if x.patente != a.patente]
                guardar_autos(autos_actualizados)
                cargar_lista_autos()
                mensaje_accion.config(text=f"Auto {a.patente} eliminado.", fg=COLOR_EXITO)

            # Botones de edición y eliminación
            marco_botones = tk.Frame(frame, bg=COLOR_BOTON)
            marco_botones.place(x=600, y=25)

            tk.Button(marco_botones, text="Editar", command=lambda a=auto: mostrar_formulario_auto(usuario_actual, ventana, modo="edicion", auto_a_editar=a), **CONFIG_BOTON_INFO).pack(pady=2)

            if not tiene_reservas:
                tk.Button(marco_botones, text="Eliminar", command=lambda a=auto: eliminar_auto_individual(a), **CONFIG_BOTON_INFO).pack(pady=2)

    # Acción del botón "Volver"
    def volver_al_menu_admin(usuario_actual, ventana):
        from interfaces.administrador.menu_admin import mostrar_menu_admin
        mostrar_menu_admin(usuario_actual, ventana)

    # Botones principales
    tk.Button(ventana, text="Agregar", command=lambda: mostrar_formulario_auto(usuario_actual, ventana, modo="alta"), **CONFIG_BOTON_FORMULARIO).place(x=600, y=180)
    tk.Button(ventana, text="Volver al menú", command=lambda: volver_al_menu_admin(usuario_actual, ventana), **CONFIG_BOTON_FORMULARIO).place(x=650, y=550)

    # Carga inicial de autos
    cargar_lista_autos()