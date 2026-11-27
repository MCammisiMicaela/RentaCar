import tkinter as tk
from recursos.estilos import *

# Muestra una ventana emergente para puntuar un auto
def abrir_ventana_puntuar(reserva, usuario_actual, ventana):
    from servicios.persistencia import cargar_json, guardar_json

    # Configura la ventana de puntuación
    ventana_puntuar = tk.Toplevel()
    ventana_puntuar.title("Puntuar auto")
    ventana_puntuar.geometry("300x200")
    ventana_puntuar.resizable(False, False)
    ventana_puntuar.configure(bg=COLOR_FONDO)

    # Título de sección
    tk.Label(ventana_puntuar, text="¿Qué puntaje le das al auto?", **CONFIG_LABEL_SECCION).pack(pady=10)

    # Variable para almacenar el puntaje seleccionado
    puntaje_var = tk.IntVar(value=0)

    # Contenedor de estrellas
    marco_estrellas = tk.Frame(ventana_puntuar, bg=COLOR_FONDO)
    marco_estrellas.pack()

    estrellas = []

    # Actualiza el color de las estrellas según el puntaje
    def actualizar_estrellas(puntaje):
        for idx, lbl in enumerate(estrellas, start=1):
            if idx <= puntaje:
                lbl.config(fg=COLOR_PUNTUACION)
            else:
                lbl.config(fg=COLOR_FONDO)

    # Crea las estrellas interactivas
    for i in range(1, 6):
        lbl = tk.Label(
            marco_estrellas,
            text="⭐",
            font=("Segoe UI", 16),
            bg = COLOR_TEXTO,
            fg=COLOR_FONDO,
            cursor="hand2"
        )
        lbl.pack(side="left", padx=5)
        lbl.bind("<Button-1>", lambda e, idx=i: [puntaje_var.set(idx), actualizar_estrellas(idx)])
        estrellas.append(lbl)

    # Inicializa las estrellas apagadas
    actualizar_estrellas(puntaje_var.get())

    # Mensaje dinámico para mostrar errores o éxito
    mensaje = tk.Label(ventana_puntuar, text="", font=("Segoe UI", 9), bg=COLOR_FONDO)
    mensaje.pack(pady=10)

    # Acción del botón "Confirmar"
    def confirmar():
        from interfaces.cliente.mis_reservas import mostrar_mis_reservas
        from servicios.gestion_reservas import calificar_reserva

        puntaje = puntaje_var.get()
        if puntaje == 0:
            mensaje.config(text="Seleccioná al menos una estrella.", fg=COLOR_ERROR)
            return

        # Registra la calificación en la reserva
        exito, respuesta = calificar_reserva(reserva["id_reserva"], puntaje, usuario=usuario_actual.usuario)
        mensaje.config(text=respuesta, fg=COLOR_EXITO if exito else COLOR_ERROR)

        # Si fue exitoso, cierra la ventana y actualiza el historial
        if exito:
            ventana_puntuar.after(1500, lambda: [ventana_puntuar.destroy(), mostrar_mis_reservas(usuario_actual, ventana)])

    # Botón para confirmar la puntuación
    tk.Button(ventana_puntuar, text="Confirmar", command=confirmar, **CONFIG_BOTON_MINI).pack()