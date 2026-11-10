
# Bimo — Aplicación de bienestar emocional

## 1. Descripción del proyecto

Bimo es una aplicación web de acompañamiento emocional orientada al bienestar de las personas en el contexto laboral. Utiliza una mascota virtual que acompaña al usuario en el registro de su bienestar y entrega mensajes y sugerencias de autocuidado mediante respuestas predefinidas.

El proyecto busca facilitar el reconocimiento del estado emocional y favorecer la identificación de tendencias personales, resguardando la privacidad de los registros individuales.

## 2. Objetivo del MVP

Desarrollar una aplicación web que permita registrar el bienestar emocional, consultar la evolución personal e interactuar con una mascota virtual mediante reglas y respuestas predefinidas.

## 3. Funcionalidades implementadas

- Inicio de sesión y cierre de sesión.
- Autenticación de usuarios mediante correo electrónico y contraseña.
- Gestión de perfiles de usuario: administrador, trabajador y organizacional.
- Creación y administración de organizaciones.
- Creación de usuarios desde el panel de administración.
- Asociación de usuarios a una organización.
- Visualización de usuarios y organizaciones registrados.
- Registro del bienestar emocional del trabajador.
- Respuestas predefinidas de la mascota virtual Bimo.

## 4. Funcionalidades pendientes de desarrollo

- Sistema de invitaciones para la activación de cuentas.
- Panel organizacional con indicadores agregados.
- Visualización de tendencias de bienestar.
- Medidas de privacidad y umbrales mínimos para la presentación de comparaciones organizacionales.
- Mejoras en la administración de usuarios y organizaciones.
- Pruebas y validación integral del MVP.
- Despliegue de la aplicación en un entorno accesible externamente.

## 5. Tecnologías

- **Lenguaje:** Python.
- **Backend:** Flask.
- **Frontend:** HTML, CSS y JavaScript.
- **Base de datos:** SQLite.
- **Gestión de datos:** Flask-SQLAlchemy.
- **Autenticación:** Flask-Login.
- **Seguridad de contraseñas:** Werkzeug Security.
- **Editor de código:** Visual Studio Code.
- **Control de versiones:** Git y GitHub.
- **Diseño de interfaces:** Figma.

## 6. Estado actual del proyecto

El proyecto se encuentra en etapa de desarrollo del producto mínimo viable (MVP).

Actualmente se cuenta con una primera implementación funcional que incorpora autenticación de usuarios, perfiles diferenciados, administración de organizaciones, creación de usuarios y registro individual de bienestar emocional.

Se continúa trabajando en la ampliación de funcionalidades, la validación de los permisos según perfil y el desarrollo de los indicadores organizacionales.

## 7. Privacidad y alcance

Bimo tiene un enfoque preventivo y de bienestar emocional. No realiza diagnósticos clínicos.

Los registros personales deben mantenerse privados y los indicadores organizacionales deben presentarse de forma agregada, aplicando medidas para reducir el riesgo de identificación de las personas.

## 8. Uso de inteligencia artificial

Se utilizaron herramientas de asistencia basadas en inteligencia artificial como apoyo en tareas de planificación, redacción y diseño del proyecto.

La interacción prevista de Bimo en el MVP funciona mediante reglas y respuestas predefinidas, sin utilizar IA generativa para generar sus respuestas.

## 9. Ejecución local

Para ejecutar el proyecto en un entorno local:

1. Instalar Python.
2. Crear y activar un entorno virtual.
3. Instalar las dependencias:

   `pip install -r requirements.txt`

4. Ejecutar la aplicación:

   `python app.py`

5. Abrir en el navegador:

   `http://127.0.0.1:5000`

La base de datos SQLite se genera localmente al ejecutar la aplicación.
