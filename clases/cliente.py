from clases.usuario import Usuario

class Cliente(Usuario):
    def __init__(self, usuario, nombre, apellido, fecha_nacimiento, celular, contraseña, tipo="cliente", bloqueado=False):
        super().__init__(usuario, nombre, apellido, fecha_nacimiento, celular, contraseña, tipo, bloqueado)