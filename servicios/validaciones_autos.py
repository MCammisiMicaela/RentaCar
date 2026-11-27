# Valida los datos ingresados para registrar o editar un auto
def validar_auto(datos, autos_existentes=None, modo="alta"):
    errores = []
    if not datos["patente"]:
        errores.append("La patente es obligatoria.")
    if not datos["marca"]:
        errores.append("La marca es obligatoria.")
    if not datos["modelo"]:
        errores.append("El modelo es obligatorio.")
    if datos["transmision"] == "Seleccionar opción":
        errores.append("Debe seleccionar la transmisión.")
    if not datos["pasajeros"].isdigit() or int(datos["pasajeros"]) <= 0:
        errores.append("La cantidad de pasajeros debe ser un número positivo.")
    if datos["categoria"] == "Seleccionar opción":
        errores.append("Debe seleccionar la categoría.")
    if not datos["color"]:
        errores.append("El color es obligatorio.")
    try:
        precio = float(datos["precio_por_dia"])
        if precio <= 0:
            errores.append("El precio debe ser un número positivo.")
    except:
        errores.append("El precio debe ser un número.")
    if not datos["foto"]:
        errores.append("Debe seleccionar una foto.")
    if modo == "alta" and autos_existentes:
        if any(auto.patente == datos["patente"] for auto in autos_existentes):
            errores.append("Ya existe un auto con esa patente.")
    return (False, errores) if errores else (True, [])