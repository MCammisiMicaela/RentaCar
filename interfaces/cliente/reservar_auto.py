"""Confirmación de alquiler desde el buscador de vehículos."""
from tkinter import messagebox
from servicios.gestion_reservas import crear_reserva


def confirmar_reserva(auto, fecha_entrega, fecha_devolucion, usuario_actual, ventana):
    exito, mensaje = crear_reserva(
        usuario_actual.usuario, auto.patente,
        fecha_entrega.isoformat(), fecha_devolucion.isoformat()
    )
    if not exito:
        messagebox.showerror("No se pudo reservar", mensaje)
        return
    messagebox.showinfo("Reserva confirmada", mensaje)
    from interfaces.cliente.buscar_auto import mostrar_buscar_autos
    mostrar_buscar_autos(usuario_actual, ventana, fecha_entrega, fecha_devolucion)
