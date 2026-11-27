# RentaCar 🚗

**Sistema de alquiler de vehículos | Aplicación de escritorio en Python**

RentaCar es un proyecto de desarrollo de software que diseñé e implementé para gestionar vehículos, clientes y operaciones de alquiler desde una aplicación de escritorio. El sistema reúne la administración del catálogo de autos con la experiencia de reserva del cliente, el seguimiento de alquileres y la calificación de vehículos.

El desarrollo está organizado en módulos y utiliza **programación orientada a objetos (POO)**, interfaces con **Tkinter** y persistencia local mediante archivos **JSON**. La autenticación incorpora un mecanismo de protección de contraseñas con **PBKDF2-HMAC-SHA256**.

## Funcionalidades

### Gestión de usuarios y seguridad

- Registro e inicio de sesión de clientes.
- Acceso diferenciado para clientes, administradores y administrador general.
- Gestión de clientes y administradores desde sus respectivos paneles.
- Consulta y modificación de datos personales.
- Cambio de contraseña con validación de la contraseña actual.
- Bloqueo de cuentas desde las funciones de administración.
- Almacenamiento de contraseñas mediante PBKDF2-HMAC-SHA256, con sal aleatoria y comparación segura de hashes.
- Creación del administrador inicial a partir de una variable de entorno, sin credenciales predeterminadas incorporadas al código.

### Administración de vehículos

- Registro, edición, consulta y eliminación de vehículos.
- Gestión de marca, modelo, patente, categoría, transmisión, pasajeros, color, fotografía y precio por día.
- Bloqueo y desbloqueo de vehículos.
- Configuración de períodos de indisponibilidad mediante un calendario.
- Visualización de calificaciones promedio y consulta del historial de reservas.

### Experiencia del cliente

- Selección de fechas de entrega y devolución.
- Búsqueda de vehículos disponibles para el período seleccionado.
- Filtros por categoría, transmisión y precio.
- Ordenamiento por precio o calificación.
- Creación y cancelación de reservas.
- Consulta de reservas propias, sus estados y el importe calculado a partir del período de alquiler.
- Calificación de vehículos de **1 a 5 estrellas** después de finalizar una reserva.

## Tecnologías utilizadas

| Tecnología | Aplicación |
| --- | --- |
| **Python 3.12** | Lógica del sistema y programación orientada a objetos |
| **Tkinter** | Interfaz gráfica de escritorio |
| **tkcalendar** | Selección de fechas y calendarios |
| **Pillow** | Visualización y tratamiento de imágenes |
| **JSON** | Persistencia local de usuarios, autos y reservas |
| **hashlib, hmac y secrets** | Derivación y verificación segura de contraseñas |
| **Git y GitHub** | Control de versiones y documentación |

## Arquitectura del proyecto

Organicé el sistema separando las responsabilidades de presentación, entidades, reglas de negocio, validaciones y persistencia.

```text
RentaCar/
├── clases/                    # Entidades: Usuario, Cliente, Administrador, Auto y Reserva
├── config/                    # Inicialización del administrador
├── datos/                     # Almacenamiento JSON local (excluido de Git)
├── interfaces/
│   ├── administrador/         # Gestión de vehículos, clientes y reservas
│   ├── cliente/               # Búsqueda, reservas y puntuaciones
│   └── comunes/               # Login, registro y cuenta personal
├── recursos/                  # Imágenes y estilos visuales
├── servicios/                 # Reglas de negocio, seguridad y persistencia
├── tests/                     # Pruebas de integración y compatibilidad
├── main.py                    # Punto de entrada
└── requirements.txt           # Dependencias externas
```

La estructura permite mantener separadas las interfaces de la lógica del sistema. Las entidades se representan mediante clases, mientras que los servicios implementan las operaciones de usuarios, vehículos, reservas y calificaciones.

## Instalación y ejecución

**Requisitos:** Python 3.12 con Tkinter disponible, Git y un entorno de escritorio compatible.

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/MCammisiMicaela/RentaCar.git
   cd RentaCar
   ```

2. Instalar las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. En una instalación nueva, configurar la contraseña inicial del administrador general. En **PowerShell**:

   ```powershell
   $clave = Read-Host "Contraseña inicial del administrador" -AsSecureString
   $env:RENTACAR_ADMIN_PASSWORD = [System.Net.NetworkCredential]::new("", $clave).Password
   python main.py
   Remove-Item Env:\RENTACAR_ADMIN_PASSWORD
   ```

   La contraseña inicial requiere al menos **12 caracteres**, incluyendo letras y números. El usuario administrador inicial es `admin_general`. Si ya existe, no es necesario volver a configurar esta variable.

4. Para ejecuciones posteriores, iniciar la aplicación desde la raíz del proyecto:

   ```bash
   python main.py
   ```

Los archivos de datos se crean y mantienen localmente dentro de `datos/`. Su contenido, junto con la configuración privada, está excluido del control de versiones.

## Reglas principales de negocio

- Los rangos de reserva se verifican para evitar superposiciones entre alquileres activos.
- Los vehículos bloqueados o con períodos de indisponibilidad no se ofrecen para esas fechas.
- Las reservas pueden estar **activas, finalizadas o canceladas**.
- La calificación corresponde a una reserva finalizada y admite una puntuación de **1 a 5 estrellas**.
- Las reservas y las calificaciones se asocian con el usuario y el vehículo correspondiente.
- La aplicación permite leer registros de vehículos y reservas con campos utilizados en versiones anteriores del proyecto.

## Pruebas

El proyecto incluye comprobaciones automáticas de autenticación, compatibilidad de datos, reservas, cancelaciones y calificaciones.

```bash
python tests/test_integracion.py
```

## Sobre el proyecto

Desarrollé RentaCar para aplicar conocimientos de **Python, POO, diseño de interfaces, validación de datos, organización modular y lógica de negocio** a un caso práctico. El proyecto evolucionó a partir de una primera implementación funcional de alquileres y calificaciones, y luego incorporé una estructura más modular y mejoras de seguridad.

---

**Desarrollo:** [Micaela Cammisi](https://github.com/MCammisiMicaela)
**Repositorio:** [github.com/MCammisiMicaela/RentaCar](https://github.com/MCammisiMicaela/RentaCar)
