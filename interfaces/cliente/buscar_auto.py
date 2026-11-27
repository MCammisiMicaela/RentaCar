import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import date, datetime
from recursos.estilos import *
from servicios.gestion_autos import cargar_autos
from servicios.gestion_reservas import auto_disponible, cargar_reservas
from servicios.persistencia import cargar_json
from interfaces.cliente.reservar_auto import confirmar_reserva
import os

# Ruta base para las imágenes de autos
RUTA_ICONOS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "recursos", "iconos"))
IMAGEN_POR_DEFECTO = os.path.join(RUTA_ICONOS, "auto_generico.png")

# Carga una imagen de auto, o una genérica si no existe
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

# Muestra la interfaz de búsqueda de autos con filtros y resultados
def mostrar_buscar_autos(usuario_actual, ventana, fecha_desde=None, fecha_hasta=None):
    # Limpia la ventana actual
    for widget in ventana.winfo_children():
        widget.destroy()
    ventana.title("Buscar autos")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    # Carga el fondo visual
    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize(TAMANIO_FONDO)
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.image = fondo_img
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar fondo:", e)

    autos_filtrados = []

    # Filtros de búsqueda: fechas, categoría, transmisión, precio
    marco_filtros = tk.Frame(ventana, bg=COLOR_FONDO)
    marco_filtros.place(x=10, y=280, width=240, height=400)

    tk.Label(marco_filtros, text="Filtros", **CONFIG_LABEL_SECCION).place(x=10, y=10)

    tk.Label(marco_filtros, text="Desde:", **CONFIG_LABEL_FILTRO).place(x=10, y=40)
    entry_desde = DateEntry(marco_filtros, date_pattern= "yyyy-mm-dd", width=18, font=("Segoe UI", 9))
    entry_desde.place(x=100, y=40)

    tk.Label(marco_filtros, text="Hasta:", **CONFIG_LABEL_FILTRO).place(x=10, y=80)
    entry_hasta = DateEntry(marco_filtros, date_pattern="yyyy-mm-dd", width=18, font=("Segoe UI", 9))
    entry_hasta.place(x=100, y=80)

    tk.Label(marco_filtros, text="Categoría:", **CONFIG_LABEL_FILTRO).place(x=10, y=120)
    categoria_var = tk.StringVar()
    opciones_categoria = ["Seleccionar opción", "Chico", "Mediano", "Camioneta"]
    categoria_var.set("Seleccionar opción")
    ttk.Combobox(marco_filtros, textvariable=categoria_var, values=opciones_categoria, width=18, font=("Segoe UI", 9)).place(x=100, y=120)

    tk.Label(marco_filtros, text="Transmisión:", **CONFIG_LABEL_FILTRO).place(x=10, y=150)
    transmision_var = tk.StringVar()
    opciones_caract = ["Seleccionar opción", "Manual", "Automático"]
    transmision_var.set("Seleccionar opción")
    ttk.Combobox(marco_filtros, textvariable=transmision_var, values=opciones_caract, width=18, font=("Segoe UI", 9)).place(x=100, y=150)

    tk.Label(marco_filtros, text="Min $:", **CONFIG_LABEL_FILTRO).place(x=10, y=180)
    entry_min = tk.Entry(marco_filtros, width=21, font=("Segoe UI", 9))
    entry_min.place(x=100, y=180)

    tk.Label(marco_filtros, text="Max $:", **CONFIG_LABEL_FILTRO).place(x=10, y=210)
    entry_max = tk.Entry(marco_filtros, width=21, font=("Segoe UI", 9))
    entry_max.place(x=100, y=210)

    # Botón para aplicar filtros seleccionados
    tk.Button(marco_filtros, text="Filtrar", command=lambda: actualizar_resultados(), **CONFIG_BOTON_FORMULARIO).place(x=60, y=250)


    tk.Label(ventana, text="Ordenar por:", **CONFIG_LABEL_FORMULARIO).place(x=10, y=140)

    # Botones para ordenar los resultados
    tk.Button(ventana, text="Precio más bajo", command=lambda: ordenar_por(autos_filtrados, "precio_asc"), **CONFIG_BOTON_MINI).place(x=10, y=180)
    tk.Button(ventana, text="Precio más alto", command=lambda: ordenar_por(autos_filtrados, "precio_desc"), **CONFIG_BOTON_MINI).place(x=10, y=220)
    tk.Button(ventana, text="Mejor puntuación", command=lambda: ordenar_por(autos_filtrados, "puntuacion"), **CONFIG_BOTON_MINI).place(x=10, y=260)

    # Área con scroll para mostrar los autos disponibles
    canvas_resultados = tk.Canvas(ventana, bg=COLOR_BOTON)
    canvas_resultados.place(x=270, y=140, width=500, height=400)
    scrollbar_resultados = tk.Scrollbar(ventana, orient="vertical", command=canvas_resultados.yview)
    scrollbar_resultados.place(x=770, y=140, height=400)

    marco_resultados = tk.Frame(canvas_resultados, bg=COLOR_BOTON)
    canvas_resultados.create_window((0, 0), window=marco_resultados, anchor="nw")
    canvas_resultados.configure(yscrollcommand=scrollbar_resultados.set)

    marco_resultados.bind("<Configure>", lambda e: canvas_resultados.configure(scrollregion=canvas_resultados.bbox("all")))
    canvas_resultados.bind_all("<MouseWheel>", lambda e: canvas_resultados.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def esta_bloqueado(auto, desde, hasta):
        if not auto or not auto.disponibilidad:
            return False
        for periodo in auto.disponibilidad:
            d = datetime.strptime(periodo["desde"], "%Y-%m-%d").date()
            h = datetime.strptime(periodo["hasta"], "%Y-%m-%d").date()
            if d <= desde <= h or d <= hasta <= h or (desde <= d and hasta >= h):
                return True
        return False

    def esta_reservado(patente, desde, hasta, reservas):
        for r in reservas:
            if r["patente"].strip().upper() != patente.strip().upper():
                continue
            if r["estado"] not in ("activa", "pendiente"):
                continue
            d = datetime.strptime(r["desde"], "%Y-%m-%d").date()
            h = datetime.strptime(r["hasta"], "%Y-%m-%d").date()
            if d <= desde <= h or d <= hasta <= h or (desde <= d and hasta >= h):
                return True
        return False

    # Aplica los filtros seleccionados y devuelve autos disponibles
    def aplicar_filtros():
        # Validación de fechas
        try:
            desde = entry_desde.get_date()
            hasta = entry_hasta.get_date()
        except Exception:
            messagebox.showerror("Error de formato", "Las fechas ingresadas no son válidas.")
            return []

        hoy = date.today()
        if desde < hoy:
            messagebox.showwarning("Fecha inválida", "La fecha de inicio no puede ser anterior a hoy.")
            return []
        if hasta < hoy:
            messagebox.showwarning("Fecha inválida", "La fecha de fin no puede ser anterior a hoy.")
            return []
        if desde > hasta:
            messagebox.showwarning("Rango inválido", "La fecha de inicio debe ser anterior o igual a la de fin.")
            return []

        # Filtros por categoría, transmisión y precio
        autos = cargar_autos()
        reservas = cargar_reservas()
        min_precio = entry_min.get()
        max_precio = entry_max.get()
        categoria = categoria_var.get()
        caract = transmision_var.get()

        filtrados = []
        try:
            minimo = float(min_precio) if min_precio.strip() else None
            maximo = float(max_precio) if max_precio.strip() else None
        except ValueError:
            messagebox.showerror("Precio inválido", "Ingresá valores numéricos para los precios.")
            return []
        for auto in autos:
            # Excluir autos bloqueados directamente
            if auto.bloqueado:
                continue

            # Excluir autos bloqueados por disponibilidad
            if esta_bloqueado(auto, desde, hasta):
                continue

            # Excluir autos ya reservados en ese rango.
            if not auto_disponible(auto.patente, desde.isoformat(), hasta.isoformat(), reservas):
                continue

            if categoria != "Seleccionar opción" and auto.categoria != categoria:
                continue
            if caract != "Seleccionar opción" and auto.transmision != caract:
                continue
            if minimo is not None and auto.precio_por_dia < minimo:
                continue
            if maximo is not None and auto.precio_por_dia > maximo:
                continue
            filtrados.append(auto)

        return filtrados

    # Actualiza la lista de autos mostrados en pantalla
    def actualizar_resultados():
        filtrados = aplicar_filtros()
        autos_filtrados.clear()
        autos_filtrados.extend(filtrados)
        mostrar_resultados(autos_filtrados)


    # Muestra cada auto con imagen, datos y botón de reserva
    def mostrar_resultados(lista_autos):
        for widget in marco_resultados.winfo_children():
            widget.destroy()

        # Calcula precio total y puntuación promedio
        try:
            desde = entry_desde.get_date()
            hasta = entry_hasta.get_date()
            dias = max((hasta - desde).days + 1, 1)
        except (ValueError, TypeError):
            desde = hasta = date.today()
            dias = 1

        for i, auto in enumerate(lista_autos):
            # Calcular promedio de puntuación
            reservas = cargar_reservas()
            puntuaciones = [r.get("puntaje") for r in reservas if r.get("patente") == auto.patente and r.get("puntaje") is not None]
            if puntuaciones:
                promedio = round(sum(puntuaciones) / len(puntuaciones), 1)
                estrellas = "⭐" * int(round(promedio))
                texto_puntuacion = f"{estrellas} ({promedio}/5)"
            else:
                texto_puntuacion = "Sin puntuación"

            frame_auto = tk.Frame(marco_resultados, bg=COLOR_BOTON, bd=1, relief="groove")
            frame_auto.grid(row=i, column=0, padx=6, pady=6, sticky="ew")

            # Imagen
            img_tk = cargar_imagen_auto(auto.foto)
            if img_tk:
                lbl_img = tk.Label(frame_auto, image=img_tk, bg=COLOR_BOTON)
                lbl_img.image = img_tk
                lbl_img.grid(row=0, column=0, rowspan=4, padx=8, pady=8)
            else:
                tk.Label(frame_auto, text="Sin imagen", fg="red", bg=COLOR_BOTON).grid(row=0, column=0, rowspan=4, padx=8, pady=8)

            # Marca y modelo
            tk.Label(
                frame_auto,
                text=f"{auto.marca} {auto.modelo} ({auto.color})",
                justify="left",
                font=("Segoe UI", 10, "bold"),
                bg=COLOR_BOTON
            ).grid(row=0, column=1, sticky="w", padx=8, pady=(6,2))

            # Info adicional
            info = f"Categoría: {auto.categoria} | Pasajeros: {auto.pasajeros}\nTransmisión: {auto.transmision}"
            tk.Label(frame_auto, text=info, justify="left", font=("Segoe UI", 9), bg=COLOR_BOTON).grid(row=1, column=1, sticky="w", padx=8, pady=(2,2))

            # Promedio de puntuación
            tk.Label(frame_auto, text=f"Puntuación: {texto_puntuacion}", font=("Segoe UI", 9), bg=COLOR_BOTON, fg=COLOR_PUNTUACION).grid(row=2, column=1, sticky="w", padx=8, pady=(2,2))

            # Precio por día
            tk.Label(frame_auto, text=f"${auto.precio_por_dia}/día", font=("Segoe UI", 10), bg=COLOR_BOTON).grid(row=0, column=2, sticky="e", padx=8, pady=(6,2))

            # Precio total
            tk.Label(
                frame_auto,
                text=f"Total: ${auto.precio_por_dia * dias}",
                font=("Segoe UI", 10, "bold"),
                bg=COLOR_BOTON
            ).grid(row=1, column=2, sticky="e", padx=8, pady=(2,2))

            # Botón de reservar
            tk.Button(
                frame_auto,
                text="Reservar ahora",
                command=lambda a=auto: confirmar_reserva(a, desde, hasta, usuario_actual, ventana),
                **CONFIG_BOTON_INFO
            ).grid(row=2, column=2, sticky="e", padx=8, pady=(2,6))

        marco_resultados.update_idletasks()
        canvas_resultados.configure(scrollregion=canvas_resultados.bbox("all"))

    # Ordena los autos según el criterio seleccionado
    def ordenar_por(lista_autos, criterio):
        if not lista_autos:
            messagebox.showinfo("Sin resultados", "Primero aplicá un filtro para ver autos disponibles.")
            return

        reservas = cargar_reservas()

        if criterio == "precio_asc":
            autos_ordenados = sorted(lista_autos, key=lambda a: a.precio_por_dia)
        elif criterio == "precio_desc":
            autos_ordenados = sorted(lista_autos, key=lambda a: a.precio_por_dia, reverse=True)
        elif criterio == "puntuacion":
            def promedio_puntuacion(auto):
                puntuaciones = [r.get("puntaje") for r in reservas if r.get("patente") == auto.patente and r.get("puntaje") is not None]
                return sum(puntuaciones) / len(puntuaciones) if puntuaciones else 0
            autos_ordenados = sorted(lista_autos, key=promedio_puntuacion, reverse=True)
        else:
            autos_ordenados = lista_autos

        mostrar_resultados(autos_ordenados)


    # Fechas desde el menú cliente se aplican automáticamente
    if fecha_desde:
        entry_desde.set_date(fecha_desde)
    if fecha_hasta:
        entry_hasta.set_date(fecha_hasta)
    if fecha_desde and fecha_hasta:
        autos_filtrados.clear()
        autos_filtrados.extend(aplicar_filtros())
        mostrar_resultados(autos_filtrados)

    # Botón para volver al menú principal del cliente
    def volver_al_menu_cliente(usuario_actual, ventana):
        from interfaces.cliente.menu_cliente import mostrar_menu_cliente
        mostrar_menu_cliente(usuario_actual, ventana)

    tk.Button(ventana, text="Volver al menú", command=lambda: volver_al_menu_cliente(usuario_actual, ventana), **CONFIG_BOTON_FORMULARIO).place(x=650, y=550)
