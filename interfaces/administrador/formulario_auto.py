from servicios.gestion_reservas import cargar_reservas
import tkinter as tk
from tkinter import filedialog
import shutil
from uuid import uuid4
from PIL import Image, ImageTk
from recursos.estilos import *
from tkcalendar import Calendar
from datetime import datetime, timedelta, date
from servicios.gestion_autos import cargar_autos, guardar_autos, buscar_auto_por_patente
from servicios.validaciones_autos import validar_auto
from clases.auto import Auto
import os

# Muestra el formulario para alta o edición de autos
def mostrar_formulario_auto(usuario_actual, ventana, modo="edicion", auto_a_editar=None):
    # Limpia la ventana actual
    for widget in ventana.winfo_children():
        widget.destroy()

    # Configura la ventana
    ventana.deiconify()
    ventana.title("Agregar auto" if modo == "alta" else "Editar auto")
    ventana.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
    ventana.resizable(False, False)

    # Carga el fondo visual
    try:
        fondo = Image.open(RUTA_FONDO_LIMPIO).resize(TAMANIO_FONDO)
        imagen_fondo = ImageTk.PhotoImage(fondo)
        etiqueta_fondo = tk.Label(ventana, image=imagen_fondo)
        etiqueta_fondo.image = imagen_fondo
        ventana.imagen_fondo = imagen_fondo
        etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Error al cargar fondo:", e)

    y_actual = 60
     # Contenedor principal
    marco = tk.Frame(ventana, bg=COLOR_FONDO, width=800, height=700)
    marco.place(x=30, y=20)

    # Título del formulario
    tk.Label(marco, text="Alta de auto" if modo == "alta" else "Edición de auto", **CONFIG_LABEL_TITULO).place(x=30, y=10)

    # Diccionario para almacenar los campos
    campos = {}

    # Función auxiliar para crear campos de texto
    def crear_campo(etiqueta, y, estado="normal", valor=""):
        tk.Label(marco, text=etiqueta, **CONFIG_LABEL_FORMULARIO).place(x=30, y=y)
        entrada = tk.Entry(marco, **CONFIG_ENTRY)
        entrada.place(x=250, y=y)
        entrada.insert(0, valor)
        entrada.config(state=estado)
        return entrada

    # Campo: Patente (no editable en edición)
    campos["patente"] = crear_campo("Patente:", y_actual, estado="normal" if modo == "alta" else "disabled", valor=getattr(auto_a_editar, "patente", ""))

    tk.Label(marco, text="Fechas no disponibles:", **CONFIG_LABEL_FORMULARIO).place(x=500, y=y_actual)

    # Calendario de fechas no disponibles
    calendario = Calendar(marco, **CONFIG_CALENDARIO)
    calendario._showtooltip = lambda *args, **kwargs: None
    calendario.place(x=500, y=y_actual + 30)

    if hasattr(calendario, "tooltipcalendar"):
        calendario.tooltipcalendar.destroy()
        calendario.tooltipcalendar = None
    calendario.tag_config('rango', background="#66A6B6", foreground='black')
    calendario.tag_config('nd', background="#D8AFAF", foreground='black')
    calendario.tag_config('bloqueado', background="#8F8080", foreground='black')
    fechas_no_disponibles = set()

    from servicios.persistencia import cargar_json
    reservas = cargar_reservas()
    fechas_no_disponibles = set()
    fechas_reservadas = set()

    # Marca fechas bloqueadas por disponibilidad manual
    if auto_a_editar and auto_a_editar.disponibilidad:
        for periodo in auto_a_editar.disponibilidad:
            desde = datetime.strptime(periodo["desde"], "%Y-%m-%d").date()
            hasta = datetime.strptime(periodo["hasta"], "%Y-%m-%d").date()
            dia = desde
            while dia <= hasta:
                fechas_no_disponibles.add(dia.strftime("%Y-%m-%d"))
                calendario.calevent_create(dia, '', 'bloqueado')
                dia += timedelta(days=1)

    # Marca fechas bloqueadas por reservas existentes
    if auto_a_editar:
        for reserva in reservas:
            if reserva["patente"] == auto_a_editar.patente and reserva["estado"] in ("activa", "finalizada"):
                desde_r = datetime.strptime(reserva["desde"], "%Y-%m-%d").date()
                hasta_r = datetime.strptime(reserva["hasta"], "%Y-%m-%d").date()
                dia_r = desde_r
                while dia_r <= hasta_r:
                    fechas_reservadas.add(dia_r.strftime("%Y-%m-%d"))
                    calendario.calevent_create(dia_r, '', 'nd')
                    dia_r += timedelta(days=1)

    # Función para marcar o desmarcar fechas en el calendario
    def marcar_fecha(evento=None):
        fecha = calendario.get_date()
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        fecha_str = fecha_obj.strftime("%Y-%m-%d")

        if fecha_obj < hoy:
            etiqueta_mensaje.config(text="No se pueden seleccionar fechas pasadas.", fg=COLOR_ERROR)
            return

        # Evita modificar fechas reservadas
        if fecha_str in fechas_reservadas:
            etiqueta_mensaje.config(text="Esta fecha está reservada y no se puede modificar.", fg=COLOR_ERROR)
            return

        eventos = calendario.get_calevents(date=fecha_obj)
        bloqueada = any('bloqueado' in calendario.calevent_cget(ev_id, 'tags') for ev_id in eventos)
        seleccionada = fecha_str in fechas_no_disponibles

        # --- Si está bloqueada manualmente, la desbloqueamos ---
        if bloqueada or seleccionada:
            for ev_id in eventos:
                calendario.calevent_remove(ev_id)
            if fecha_str in fechas_no_disponibles:
                fechas_no_disponibles.remove(fecha_str)
            etiqueta_mensaje.config(text=f"Fecha {fecha_str} desbloqueada.", fg=COLOR_EXITO)
        else:
            # --- Si no está bloqueada, la marcamos como no disponible ---
            fechas_no_disponibles.add(fecha_str)
            calendario.calevent_create(fecha_obj, None, 'bloqueado')
            etiqueta_mensaje.config(text=f"Fecha {fecha_str} bloqueada manualmente.", fg=COLOR_EXITO)

    calendario.bind("<<CalendarSelected>>", marcar_fecha)

    # Fecha actual
    hoy = date.today()
    calendario.selection_set(hoy)  # Selecciona el día actual por defecto

    # Bloquea días pasados
    primer_dia = date(hoy.year, hoy.month - 1 if hoy.month > 1 else 1, 1)
    ultimo_dia = hoy - timedelta(days=1)

    dia_actual = primer_dia
    while dia_actual <= ultimo_dia:
        calendario.calevent_create(dia_actual, 'No disponible', 'nd')
        dia_actual += timedelta(days=1)

    # Campos técnicos del auto
    y_actual += 40
    campos["marca"] = crear_campo("Marca:", y_actual, valor=getattr(auto_a_editar, "marca", ""))

    y_actual += 40
    campos["modelo"] = crear_campo("Modelo:", y_actual, valor=getattr(auto_a_editar, "modelo", ""))

    y_actual += 40
    tk.Label(marco, text="Transmisión:", **CONFIG_LABEL_FORMULARIO).place(x=30, y=y_actual)
    transmision_var = tk.StringVar()
    opciones_transmision = ["Seleccionar opción", "Manual", "Automático"]
    valor_transmision = getattr(auto_a_editar, "transmision", None)
    transmision_var.set(valor_transmision if valor_transmision in opciones_transmision else "Seleccionar opción")
    menu_transmision = tk.OptionMenu(marco, transmision_var, *opciones_transmision)
    menu_transmision.config(width=18)
    menu_transmision.place(x=250, y=y_actual)
    campos["transmision"] = transmision_var

    y_actual += 40
    campos["pasajeros"] = crear_campo("Cantidad de pasajeros:", y_actual, valor=str(getattr(auto_a_editar, "pasajeros", "")))

    y_actual += 40
    tk.Label(marco, text="Categoría:", **CONFIG_LABEL_FORMULARIO).place(x=30, y=y_actual)
    categoria_var = tk.StringVar()
    opciones_categoria = ["Seleccionar opción", "Chico", "Mediano", "Camioneta"]
    valor_categoria = getattr(auto_a_editar, "categoria", None)
    categoria_var.set(valor_categoria if valor_categoria in opciones_categoria else "Seleccionar opción")
    menu_categoria = tk.OptionMenu(marco, categoria_var, *opciones_categoria)
    menu_categoria.config(width=18)
    menu_categoria.place(x=250, y=y_actual)
    campos["categoria"] = categoria_var

    y_actual += 40
    campos["color"] = crear_campo("Color:", y_actual, valor=getattr(auto_a_editar, "color", ""))

    y_actual += 40
    campos["precio_por_dia"] = crear_campo("Precio por día:", y_actual, valor=str(getattr(auto_a_editar, "precio_por_dia", "")))
    y_actual += 40

    # Ruta fija para las imágenes
    RUTA_ICONOS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "recursos", "iconos"))
    IMAGEN_POR_DEFECTO = os.path.join(RUTA_ICONOS, "auto_generico.png")  # Asegurate de tener esta imagen en esa carpeta

    # Campo de foto
    tk.Label(marco, text="Foto:", **CONFIG_LABEL_FORMULARIO).place(x=30, y=y_actual)
    foto_var = tk.StringVar(value=getattr(auto_a_editar, "foto", "") if auto_a_editar else "")
    etiqueta_imagen = tk.Label(marco)
    etiqueta_imagen.place(x=250, y=y_actual)

    def mostrar_imagen(nombre_archivo):
        try:
            ruta_imagen = os.path.join(RUTA_ICONOS, nombre_archivo)
            if not os.path.isfile(ruta_imagen):
                ruta_imagen = IMAGEN_POR_DEFECTO
            imagen = Image.open(ruta_imagen).resize((120, 90))
            imagen_tk = ImageTk.PhotoImage(imagen)
            etiqueta_imagen.config(image=imagen_tk)
            etiqueta_imagen.image = imagen_tk
        except Exception as e:
            print("Error al cargar imagen:", e)
            etiqueta_imagen.config(text="Imagen no disponible", fg="red")

    def seleccionar_foto():
        ruta = filedialog.askopenfilename(title="Seleccionar foto", initialdir=RUTA_ICONOS, filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if ruta:
            os.makedirs(RUTA_ICONOS, exist_ok=True)
            nombre_archivo = os.path.basename(ruta)
            destino = os.path.join(RUTA_ICONOS, nombre_archivo)
            if os.path.abspath(ruta) != os.path.abspath(destino):
                if os.path.exists(destino):
                    nombre, extension = os.path.splitext(nombre_archivo)
                    nombre_archivo = f"{nombre}_{uuid4().hex[:8]}{extension}"
                    destino = os.path.join(RUTA_ICONOS, nombre_archivo)
                shutil.copy2(ruta, destino)
            foto_var.set(nombre_archivo)
            mostrar_imagen(nombre_archivo)

    # Mostrar imagen automáticamente si ya hay una cargada
    mostrar_imagen(foto_var.get() if foto_var.get() else "auto_generico.png")

    tk.Button(marco, text="Seleccionar", command=seleccionar_foto, **CONFIG_BOTON_FORMULARIO).place(x=400, y=y_actual)
    campos["foto"] = foto_var
    y_actual += 95

    # Mensaje dinámico para mostrar errores o éxito
    etiqueta_mensaje = tk.Label(marco, text="", **CONFIG_MENSAJE)
    etiqueta_mensaje.place(x=30, y=y_actual)
    y_actual += 40

    # Acción del botón "Guardar"
    def guardar_auto():
        autos = cargar_autos()
        # Recolecta datos del formulario
        datos = {
            "patente": campos["patente"].get().strip(),
            "marca": campos["marca"].get().strip(),
            "modelo": campos["modelo"].get().strip(),
            "transmision": campos["transmision"].get(),
            "pasajeros": campos["pasajeros"].get().strip(),
            "categoria": campos["categoria"].get(),
            "color": campos["color"].get().strip(),
            "precio_por_dia": campos["precio_por_dia"].get().strip(),
            "foto": campos["foto"].get().strip(),
            "bloqueado": False,
            "disponibilidad": []
        }
        # Agrupar fechas seleccionadas en períodos
        if fechas_no_disponibles:
            fechas_ordenadas = sorted(fechas_no_disponibles)
            periodos = []
            if fechas_ordenadas:
                inicio = fin = datetime.strptime(fechas_ordenadas[0], "%Y-%m-%d")
                for fecha_str in fechas_ordenadas[1:]:
                    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                    if fecha == fin + timedelta(days=1):
                        fin = fecha
                    else:
                        periodos.append({"desde": inicio.strftime("%Y-%m-%d"), "hasta": fin.strftime("%Y-%m-%d")})
                        inicio = fin = fecha
                periodos.append({"desde": inicio.strftime("%Y-%m-%d"), "hasta": fin.strftime("%Y-%m-%d")})
            datos["disponibilidad"] = periodos

        # Valida los datos
        valido, errores = validar_auto(datos, autos_existentes=autos, modo=modo)
        if not valido:
            etiqueta_mensaje.config(text=errores[0], fg=COLOR_ERROR)
            return

        autos = cargar_autos()
        if modo == "alta":
            # Verifica duplicado de patente
            if buscar_auto_por_patente(datos["patente"], autos):
                etiqueta_mensaje.config(text="Ya existe un auto con esa patente.", fg=COLOR_ERROR)
                return
            nuevo_auto = Auto(
                patente=datos["patente"],
                marca=datos["marca"],
                modelo=datos["modelo"],
                categoria=datos["categoria"],
                transmision=datos["transmision"],
                pasajeros=int(datos["pasajeros"]),
                color=datos["color"],
                precio_por_dia=float(datos["precio_por_dia"]),
                foto=datos["foto"],
                bloqueado=False,
                disponibilidad=datos["disponibilidad"]
            )
            autos.append(nuevo_auto)
            guardar_autos(autos)
            etiqueta_mensaje.config(text="Auto agregado correctamente.", fg=COLOR_EXITO)
            ventana.after(1500, lambda: volver_a_gestion_autos(usuario_actual, ventana))
        else:
            # Edición: actualiza los datos del auto
            for i, auto in enumerate(autos):
                if auto.patente == auto_a_editar.patente:
                    autos[i] = Auto(
                        patente=auto_a_editar.patente,
                        marca=datos["marca"],
                        modelo=datos["modelo"],
                        categoria=datos["categoria"],
                        transmision=datos["transmision"],
                        pasajeros=int(datos["pasajeros"]),
                        color=datos["color"],
                        precio_por_dia=float(datos["precio_por_dia"]),
                        foto=datos["foto"],
                        bloqueado=auto_a_editar.bloqueado,
                        disponibilidad=datos["disponibilidad"],
                        datos_adicionales=auto_a_editar.datos_adicionales
                    )
                    guardar_autos(autos)
                    etiqueta_mensaje.config(text="Datos del auto actualizados correctamente.", fg=COLOR_EXITO)
                    ventana.after(1500, lambda: volver_a_gestion_autos(usuario_actual, ventana))
                    break

    # Acción del botón "Volver"
    def volver_a_gestion_autos(usuario_actual, ventana):
        from interfaces.administrador.gestionar_autos import mostrar_gestion_autos
        mostrar_gestion_autos(usuario_actual, ventana)

    # Botones principales
    tk.Button(marco, text="Guardar", command=guardar_auto, **CONFIG_BOTON_FORMULARIO).place(x=300, y=500)
    tk.Button(marco, text="Volver", command=lambda: volver_a_gestion_autos(usuario_actual, ventana), **CONFIG_BOTON_FORMULARIO).place(x=300, y=540)