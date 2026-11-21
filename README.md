# Bimo — Aplicación de bienestar emocional

## 1. Descripción del proyecto

Bimo es una aplicación web de acompañamiento emocional orientada al bienestar de las personas en el contexto laboral. Utiliza una mascota virtual que acompaña al trabajador en el registro de su bienestar y entrega mensajes y sugerencias de autocuidado mediante respuestas predefinidas.

El proyecto busca facilitar el reconocimiento del estado emocional, favorecer la identificación de tendencias personales y promover el autocuidado, resguardando la privacidad de los registros individuales.

## 2. Objetivo del MVP

Desarrollar una aplicación web que permita registrar voluntariamente el bienestar emocional, consultar la evolución personal e interactuar con una mascota virtual mediante un flujo de conversación basado en reglas y respuestas predefinidas.

## 3. Funcionalidades implementadas

### F1. Acceso y perfiles de usuario

- Inicio y cierre de sesión.
- Autenticación mediante correo electrónico y contraseña.
- Gestión de tres perfiles: administrador, trabajador y usuario organizacional.
- Control de acceso según el perfil.
- Administración de organizaciones y creación de usuarios desde el panel administrador.
- Asociación de usuarios a una organización.
- Protección de las rutas según los permisos de cada perfil.

### F2. Registro de bienestar

- Registro voluntario del bienestar por parte del trabajador.
- Selección de una puntuación de bienestar de 1 a 5.
- Selección de una emoción.
- Validación de los datos ingresados.
- Asociación de cada registro al trabajador autenticado.
- Actualización del registro existente cuando se realiza un nuevo registro durante el mismo día.
- Restricción del acceso al registro de bienestar exclusivamente al perfil trabajador.

### F3. Seguimiento personal

- Visualización del historial de registros de bienestar.
- Gráfico de evolución personal basado en los últimos siete registros.
- Consulta exclusiva de los registros del trabajador autenticado.
- Protección de la información personal.
- Mensaje de privacidad que informa al trabajador que sus registros son personales.

### F4. Agente virtual Bimo

- Acompañamiento durante el registro de bienestar.
- Entrega de mensajes y sugerencias de autocuidado.
- Respuestas predefinidas según la puntuación y emoción seleccionadas.
- Funcionamiento mediante reglas, sin realizar diagnósticos clínicos.
- Diferentes respuestas para los niveles de bienestar bajo, intermedio y alto.

### Panel organizacional

- Acceso restringido al perfil organizacional.
- Visualización de la organización asociada al usuario.
- Estructura inicial del panel para futuras funcionalidades de indicadores agregados.

## 4. Funcionalidades pendientes de desarrollo

- Sistema de invitaciones para la activación de cuentas.
- Indicadores agregados de bienestar organizacional.
- Comparaciones organizacionales con umbrales mínimos de privacidad.
- Mejoras adicionales en la administración de usuarios y organizaciones.
- Ampliación de funcionalidades posteriores al MVP.

## 5. Tecnologías utilizadas

- **Lenguaje:** Python.
- **Backend:** Flask.
- **Frontend:** HTML, CSS y JavaScript.
- **Base de datos:** SQLite.
- **Gestión de datos:** Flask-SQLAlchemy.
- **Autenticación:** Flask-Login.
- **Seguridad de contraseñas:** Werkzeug Security.
- **Pruebas:** pytest.
- **Editor de código:** Visual Studio Code.
- **Control de versiones:** Git y GitHub.
- **Diseño de interfaces:** Figma.

## 6. Estructura general del proyecto

```text
BIMO/
├── app.py
├── crear_admin.py
├── requirements.txt
├── README.md
├── tests/
│   └── test_bimo.py
└── instance/
    └── bimo.db
```

La carpeta `instance/` contiene la base de datos local de la aplicación. No debe incorporarse al repositorio con información real de usuarios.

## 7. Instalación y ejecución local

### Requisitos previos

- Python instalado.
- Git instalado.
- Acceso al repositorio de GitHub.

### 7.1. Obtener el proyecto

Clonar el repositorio:

```bash
git clone https://github.com/wiiken360/bimo-bienestar-emocional.git
```

Ingresar a la carpeta:

```bash
cd bimo-bienestar-emocional
```

### 7.2. Crear un entorno virtual

En Windows:

```powershell
python -m venv .venv
```

Activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 7.3. Instalar dependencias

Con el entorno virtual activado, ejecutar:

```bash
python -m pip install -r requirements.txt
```

### 7.4. Crear el primer administrador

Para crear el primer usuario administrador de Bimo, ejecutar desde la carpeta principal del proyecto:

```bash
python crear_admin.py
```

El programa solicitará interactivamente:

- Nombre del administrador.
- Correo electrónico.
- Creación de una contraseña.
- Confirmación de la contraseña.

La contraseña debe tener al menos 10 caracteres.

El sistema verifica que el correo electrónico no esté registrado previamente y que ambas contraseñas coincidan.

Una vez completado el proceso, el administrador será creado correctamente y podrá acceder al sistema mediante el inicio de sesión.

La contraseña se almacena utilizando un mecanismo de hash seguro y no se guarda en texto plano.

### 7.5. Ejecutar la aplicación

Con el entorno virtual activado, ejecutar:

```bash
python app.py
```

Abrir el navegador en:

http://127.0.0.1:5000/login

La aplicación utiliza una base de datos SQLite que se crea automáticamente cuando se ejecuta en un entorno normal.

## 8. Ejecución de pruebas

El proyecto utiliza pytest para realizar pruebas unitarias y de integración.

Con el entorno virtual activado, ejecutar:

```bash
python -m pytest
```

Las pruebas utilizan una base de datos temporal en memoria, independiente de la base de datos de trabajo, para evitar modificar los datos reales durante su ejecución.

La suite contempla validaciones de:

- Reglas de respuesta del agente Bimo.
- Inicio de sesión y autenticación.
- Control de acceso según perfil.
- Privacidad de los registros personales.
- Validación de puntuaciones y emociones.
- Actualización de registros diarios.
- Restricción del registro de bienestar al perfil trabajador.
- Acceso al panel organizacional.
- Rechazo de contraseñas incorrectas.
- Redirección al inicio de sesión cuando no existe una sesión activa.

**Estado de las pruebas durante la preparación de la Sumativa 2: 20 pruebas aprobadas.**

## 9. Privacidad y alcance

Bimo tiene un enfoque preventivo y de bienestar emocional. No realiza diagnósticos clínicos ni reemplaza la atención de profesionales de salud mental.

Los registros personales deben mantenerse privados y solo pueden ser consultados por el trabajador al que pertenecen.

Los indicadores organizacionales futuros deberán presentarse de forma agregada, aplicando medidas que reduzcan el riesgo de identificación de las personas.

## 10. Uso de inteligencia artificial

Se utilizaron herramientas de asistencia basadas en inteligencia artificial como apoyo en tareas de planificación, redacción y diseño del proyecto.

La interacción del agente Bimo en el MVP funciona mediante reglas y respuestas predefinidas, sin utilizar IA generativa para producir sus respuestas.

## 11. Estado del proyecto

Bimo se encuentra en la etapa de desarrollo y validación de su producto mínimo viable (MVP).

Las funcionalidades F1, F2, F3 y F4 cuentan con implementación local y pruebas automatizadas. Durante el desarrollo se han fortalecido los controles de acceso, la privacidad de los registros, las validaciones del bienestar y la gestión de usuarios mediante el perfil administrador.

La aplicación puede instalarse y ejecutarse localmente siguiendo las instrucciones descritas en este documento. Asimismo, se ha verificado su funcionamiento en un entorno virtual independiente y se han ejecutado satisfactoriamente 20 pruebas automatizadas.