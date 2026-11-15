
from datetime import date
import os

from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Configuración de seguridad y sesiones
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "bimo-clave-desarrollo-cambiar-en-produccion"
)
# Configuracion de la base de datos
os.makedirs(app.instance_path, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bimo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
# Configuración del sistema de autenticación
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder."
# Modelo de organizaciones
class Organizacion(db.Model):
    __tablename__ = "organizacion"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    activa = db.Column(db.Boolean, default=True, nullable=False)


# Modelo de usuarios
class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)

    rol = db.Column(db.String(30), nullable=False)

    organizacion_id = db.Column(
        db.Integer,
        db.ForeignKey("organizacion.id"),
        nullable=True
    )

    activo = db.Column(db.Boolean, default=True, nullable=False)

    organizacion = db.relationship(
        "Organizacion",
        backref="usuarios"
    )
    # Recuperar usuario cuando existe una sesión activa
@login_manager.user_loader
def cargar_usuario(usuario_id):
    return db.session.get(Usuario, int(usuario_id))
# Modelo inicial de los registros de bienestar
class RegistroBienestar(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.Date, nullable=False)
    puntuacion = db.Column(db.Integer, nullable=False)
    emocion = db.Column(db.String(30), nullable=False)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    usuario = db.relationship(
        "Usuario",
        backref=db.backref("registros_bienestar", lazy=True)
    )

    __table_args__ = (
        db.UniqueConstraint(
            "fecha",
            "usuario_id",
            name="uq_fecha_usuario"
        ),
    )


# Crear las tablas al ejecutar la aplicación normalmente.
# Durante las pruebas se utilizará una base de datos independiente.
if os.environ.get("BIMO_TESTING") != "1":
    with app.app_context():
        db.create_all()

LOGIN_PAGINA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bimo | Iniciar sesión</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef5ff;
            color: #293653;
            text-align: center;
            padding: 50px 15px;
        }
        .tarjeta {
            background: white;
            max-width: 380px;
            margin: auto;
            padding: 30px;
            border-radius: 24px;
            box-shadow: 0 8px 25px #cbd7e8;
        }
        .mascota { font-size: 75px; }
        input {
            width: 85%;
            padding: 12px;
            margin: 10px;
            border: 1px solid #ccd5e5;
            border-radius: 10px;
        }
        button {
            background: #6387e8;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 25px;
            cursor: pointer;
        }
        .error { color: #c0392b; }
    </style>
</head>
<body>
    <div class="tarjeta">
        <div class="mascota">🐻</div>
        <h2>¡Bienvenido a Bimo!</h2>
        <p>Ingresa a tu espacio de bienestar emocional.</p>

        <form method="POST">
            <input type="email" name="correo"
                   placeholder="Correo electrónico" required>

            <input type="password" name="contrasena"
                   placeholder="Contraseña" required>

            <br>
            <button type="submit">Iniciar sesión</button>
        </form>

        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
    </div>
  
</body>
</html>
"""
PANEL_ADMIN = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bimo | Administración</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef5ff;
            color: #293653;
            padding: 30px 15px;
        }
        .contenedor {
            max-width: 750px;
            margin: auto;
        }
        .tarjeta {
            background: white;
            padding: 25px;
            margin: 20px 0;
            border-radius: 20px;
            box-shadow: 0 8px 25px #cbd7e8;
        }
        input {
            padding: 12px;
            width: 90%;
            border: 1px solid #ccd5e5;
            border-radius: 10px;
            margin: 10px 0;
        }
        button {
            background: #6387e8;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 10px;
            cursor: pointer;
        }
        .organizacion {
            background: #f4f7ff;
            padding: 12px;
            margin: 10px 0;
            border-radius: 10px;
        }
        a { color: #4568c5; }
    </style>
</head>
<body>
<div class="contenedor">

    <h1>🐻 Panel de administración Bimo</h1>
    <p>Bienvenido/a, {{ usuario.nombre }}.</p>

    <div class="tarjeta">
        <h2>🏢 Crear organización</h2>

        <form method="POST">
            <label>Nombre de la organización:</label><br>
            <input
                type="text"
                name="nombre"
                placeholder="Ejemplo: Empresa Bimo"
                maxlength="120"
                required
            >
            <br>
            <button type="submit">Crear organización</button>
        </form>

        {% if mensaje %}
            <p><strong>{{ mensaje }}</strong></p>
        {% endif %}
    </div>

    <div class="tarjeta">
        <h2>Organizaciones registradas</h2>

        {% if organizaciones %}
            {% for organizacion in organizaciones %}
                <div class="organizacion">
                    <strong>{{ organizacion.nombre }}</strong>
                    <br>
                    Estado:
                    {{ "Activa" if organizacion.activa else "Inactiva" }}
                </div>
            {% endfor %}
        {% else %}
            <p>Aún no hay organizaciones registradas.</p>
        {% endif %}
    </div>

 
<div class="tarjeta">
    <h2>👥 Crear usuario</h2>

    <form method="POST">
        <input type="hidden" name="accion" value="crear_usuario">

        <label>Nombre completo:</label>
        <input type="text" name="nombre_usuario"
               placeholder="Nombre del trabajador" required>

        <label>Correo electrónico:</label>
        <input type="email" name="correo"
               placeholder="correo@empresa.cl" required>

        <label>Contraseña inicial:</label>
        <input type="password" name="contrasena"
               minlength="10" required>

        <label>Perfil del usuario:</label>
        <select name="rol" required>
            <option value="trabajador">Trabajador</option>
            <option value="organizacional">Organizacional</option>
        </select>

        <label>Organización:</label>
        <select name="organizacion_id" required>
            <option value="">Seleccionar organización</option>
            {% for organizacion in organizaciones %}
                {% if organizacion.activa %}
                <option value="{{ organizacion.id }}">
                    {{ organizacion.nombre }}
                </option>
                {% endif %}
            {% endfor %}
        </select>

        <button type="submit">Crear usuario</button>
    </form>
</div>

<div class="tarjeta">
    <h2>👥 Usuarios registrados</h2>

    {% if usuarios %}
        {% for usuario_registrado in usuarios %}
            <div class="organizacion">
                <strong>{{ usuario_registrado.nombre }}</strong><br>
                Correo: {{ usuario_registrado.correo }}<br>
                Perfil: {{ usuario_registrado.rol }}<br>
                Organización:
                {{ usuario_registrado.organizacion.nombre
                   if usuario_registrado.organizacion else "Sin organización" }}
            </div>
        {% endfor %}
    {% else %}
        <p>Aún no hay usuarios registrados.</p>
    {% endif %}
</div>

<p><a href="{{ url_for('logout') }}">Cerrar sesión</a></p>
</div>
</body>
</html>
"""
PAGINA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bimo | Bienestar emocional</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef5ff;
            color: #293653;
            text-align: center;
            padding: 30px 15px;
        }
        .tarjeta {
            background: white;
            max-width: 480px;
            margin: 25px auto;
            padding: 25px;
            border-radius: 24px;
            box-shadow: 0 8px 25px #cbd7e8;
        }
        .mascota { font-size: 85px; }
        button {
            background: #6387e8;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 18px;
            margin: 5px;
            cursor: pointer;
            font-size: 15px;
        }
        button:hover { background: #4568c5; }
        select {
            padding: 10px;
            border-radius: 10px;
            margin: 8px;
            font-size: 15px;
        }
        .registro {
            background: #f4f7ff;
            padding: 12px;
            border-radius: 12px;
            margin: 10px 0;
        }
        .nota { color: #65718a; font-size: 13px; }
    </style>
</head>
<body>
    <h1>Mi espacio emocional</h1>

    <div class="tarjeta">
        <div class="mascota">🐻</div>
        <h2>¡Hola! Soy Bimo</h2>
        <p>Estoy aquí para acompañarte.</p>
        <p><strong>¿Cómo te sientes hoy?</strong></p>

        <form method="POST">
            <label for="puntuacion">Tu nivel de bienestar:</label>
            <br>
            <select name="puntuacion" id="puntuacion" required>
                <option value="">Elige del 1 al 5</option>
                <option value="1">1 - Muy bajo</option>
                <option value="2">2 - Bajo</option>
                <option value="3">3 - Intermedio</option>
                <option value="4">4 - Bueno</option>
                <option value="5">5 - Muy bueno</option>
            </select>

            <br>

            <label for="emocion">Selecciona una emoción:</label>
            <br>
            <select name="emocion" id="emocion" required>
                <option value="">Elige una emoción</option>
                <option value="alegria">😊 Alegría</option>
                <option value="tristeza">😔 Tristeza</option>
                <option value="estres">😣 Estrés</option>
                <option value="enojo">😠 Enojo</option>
                <option value="miedo">😨 Miedo</option>
                <option value="calma">😌 Calma</option>
                <option value="confusion">🤔 No sé qué siento</option>
            </select>

            <br>
            <button type="submit">Guardar mi registro</button>
        </form>

        {% if mensaje %}
            <p><strong>{{ mensaje }}</strong></p>
            <p>{{ consejo }}</p>
        {% endif %}
    </div>

    <div class="tarjeta">
        <h2>Mis registros recientes</h2>

        {% if registros %}
        <div class="tarjeta">
    <h3>📊 Mi evolución de bienestar</h3>

    <div style="display: flex; align-items: flex-end; gap: 12px;
                height: 180px; padding: 15px 5px;">

        {% for registro in registros|reverse %}
        <div style="flex: 1; text-align: center; height: 100%;
                    display: flex; flex-direction: column;
                    justify-content: flex-end;">

            <strong>{{ registro.puntuacion }}/5</strong>

            <div style="height: 120px; display: flex;
                        align-items: flex-end; justify-content: center;">

                <div style="width: 70%; height: {{ registro.puntuacion * 20 }}%;
                            background: #6485ee; border-radius: 7px 7px 0 0;">
                </div>

            </div>

            <small>{{ registro.fecha.strftime('%d/%m') }}</small>
        </div>
        {% endfor %}

    </div>

    <p class="nota">Evolución de tus últimos registros de bienestar.</p>
</div>
            {% for registro in registros %}
                <div class="registro">
                    <strong>{{ registro.fecha.strftime('%d-%m-%Y') }}</strong>
                    <br>
                    Bienestar: {{ registro.puntuacion }}/5
                    <br>
                    Emoción: {{ registro.emocion }}
                </div>
            {% endfor %}
        {% else %}
            <p>Aún no tienes registros guardados.</p>
        {% endif %}

<p class="nota">
    Tus registros son privados y solo tú puedes consultarlos.
</p>
    </div>
    <p><a href="{{ url_for('logout') }}">Cerrar sesión</a></p>
</body>
</html>
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.rol == "administrador":
            return redirect(url_for("panel_admin"))
        elif current_user.rol == "organizacional":
            return redirect(url_for("panel_organizacional"))
        return redirect(url_for("inicio"))

    error = None

    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        contrasena = request.form.get("contrasena", "")

        usuario = Usuario.query.filter_by(
            correo=correo,
            activo=True
        ).first()

        if usuario and check_password_hash(
            usuario.contrasena_hash,
            contrasena
        ):
            login_user(usuario)

            if usuario.rol == "administrador":
                return redirect(url_for("panel_admin"))
            elif usuario.rol == "organizacional":
                return redirect(url_for("panel_organizacional"))

            return redirect(url_for("inicio"))

        error = "Correo o contraseña incorrectos."

    return render_template_string(
        LOGIN_PAGINA,
        error=error
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
@app.route("/admin", methods=["GET", "POST"])
@login_required

def panel_admin():
    if current_user.rol != "administrador":
        return "No tienes permisos para acceder a esta sección.", 403

    mensaje = None

    if request.method == "POST":
        accion = request.form.get("accion", "crear_organizacion")

        # Crear organización
        if accion == "crear_organizacion":
            nombre = request.form.get("nombre", "").strip()

            if not nombre:
                mensaje = "Debes ingresar un nombre."
            else:
                organizacion = Organizacion(nombre=nombre)
                db.session.add(organizacion)
                db.session.commit()
                mensaje = "¡Organización creada correctamente!"

        # Crear usuario
        elif accion == "crear_usuario":
            nombre = request.form.get("nombre_usuario", "").strip()
            correo = request.form.get("correo", "").strip().lower()
            contrasena = request.form.get("contrasena", "")
            rol = request.form.get("rol", "")
            organizacion_id = request.form.get("organizacion_id", "")

            if not nombre or not correo or not contrasena:
                mensaje = "Debes completar todos los campos."

            elif len(contrasena) < 10:
                mensaje = "La contraseña debe tener al menos 10 caracteres."

            elif rol not in ["trabajador", "organizacional"]:
                mensaje = "El perfil seleccionado no es válido."

            elif Usuario.query.filter_by(correo=correo).first():
                mensaje = "Ya existe un usuario con ese correo."

            else:
                try:
                    organizacion = db.session.get(
                        Organizacion,
                        int(organizacion_id)
                    )
                except (ValueError, TypeError):
                    organizacion = None

                if organizacion is None or not organizacion.activa:
                    mensaje = "Debes seleccionar una organización activa."

                else:
                    nuevo_usuario = Usuario(
                        nombre=nombre,
                        correo=correo,
                        contrasena_hash=generate_password_hash(contrasena),
                        rol=rol,
                        organizacion_id=organizacion.id,
                        activo=True
                    )

                    db.session.add(nuevo_usuario)
                    db.session.commit()

                    mensaje = "¡Usuario creado correctamente!"

    organizaciones = Organizacion.query.order_by(
        Organizacion.id.desc()
    ).all()

    usuarios = Usuario.query.filter(
        Usuario.rol != "administrador"
    ).order_by(Usuario.id.desc()).all()

    return render_template_string(
        PANEL_ADMIN,
        usuario=current_user,
        organizaciones=organizaciones,
        usuarios=usuarios,
        mensaje=mensaje
    )


@app.route("/organizacional")
@login_required
def panel_organizacional():
    if current_user.rol != "organizacional":
        return "No tienes permisos para acceder a esta sección.", 403

    organizacion = current_user.organizacion

    if not organizacion:
        return "Tu usuario no tiene una organización asociada.", 403

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bimo | Panel organizacional</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #eef4ff;
                color: #263b60;
                text-align: center;
                padding: 40px 20px;
            }
            .contenedor {
                max-width: 650px;
                margin: auto;
                background: white;
                padding: 35px;
                border-radius: 20px;
                box-shadow: 0 8px 25px #00000012;
            }
            .tarjeta {
                background: #f3f6ff;
                padding: 20px;
                border-radius: 12px;
                margin: 25px 0;
            }
            a {
                color: #527bea;
            }
        </style>
    </head>
    <body>
        <div class="contenedor">
            <h1>🏢 Espacio organizacional Bimo</h1>
            <p>Bienvenido/a, {{ usuario.nombre }}.</p>

            <div class="tarjeta">
                <h2>{{ organizacion.nombre }}</h2>
                <p>Panel de bienestar organizacional.</p>
            </div>

            <p>
                Los indicadores generales de bienestar
                estarán disponibles en una próxima etapa.
            </p>

            <p>
                <a href="{{ url_for('logout') }}">Cerrar sesión</a>
            </p>
        </div>
    </body>
    </html>
    """, usuario=current_user, organizacion=organizacion)



def obtener_consejo(puntuacion, emocion):

    # Bienestar bajo: mensajes de contención y autocuidado
    if puntuacion <= 2:
        consejos = {
            "estres": "Parece que estás pasando por un momento exigente. Intenta hacer una pausa y respirar tranquilamente. 💙",
            "tristeza": "Está bien no sentirse bien todo el tiempo. Puedes buscar a alguien de confianza para conversar. 💙",
            "enojo": "Cuando sientas enojo, intenta tomar distancia por un momento y recuperar la calma. 🌿",
            "miedo": "No tienes que enfrentar todo a solas. Acercarte a alguien de confianza puede ayudarte. 💙",
            "alegria": "Aunque hoy tu bienestar sea bajo, puedes reconocer los momentos que te generan alegría. 🌱",
            "calma": "Intenta conservar esos pequeños momentos de tranquilidad durante tu día. 🌿",
            "confusion": "Si sientes confusión, puedes tomarte un momento para ordenar tus ideas. 💙"
        }
        return consejos.get(
            emocion,
            "Gracias por compartir cómo te sientes. Recuerda que puedes buscar apoyo cuando lo necesites. 💙"
        )

    # Bienestar intermedio
    if puntuacion == 3:
        consejos = {
            "estres": "Identifica qué situación te está generando estrés y considera realizar una pausa. 🌿",
            "tristeza": "Puedes realizar una actividad agradable o conversar con alguien de confianza. 💙",
            "enojo": "Intenta reconocer qué provocó tu enojo y busca una forma tranquila de expresarlo. 🌱",
            "miedo": "Avanza paso a paso. No necesitas resolver todo de inmediato. 💙",
            "alegria": "Reconoce aquello que te hizo sentir alegría y piensa cómo puedes repetirlo. 🌱",
            "calma": "Qué bueno que encuentres momentos de calma. Intenta mantener ese espacio para ti. 🌿",
            "confusion": "Puedes tomarte un tiempo para identificar qué necesitas en este momento. 💙"
        }
        return consejos.get(
            emocion,
            "¿Qué pequeña acción podría ayudarte a sentirte mejor hoy? 🌿"
        )

    # Bienestar alto
    consejos = {
        "estres": "Aunque tu bienestar sea positivo, recuerda darte espacios de descanso para prevenir la sobrecarga. 🌿",
        "tristeza": "Reconoce lo que estás sintiendo y continúa dedicando tiempo a actividades que te hagan bien. 💙",
        "enojo": "Es positivo reconocer tus emociones. Sigue buscando formas saludables de expresarlas. 🌱",
        "miedo": "Reconoce tus avances y recuerda que puedes afrontar los desafíos paso a paso. 💙",
        "alegria": "¡Qué bueno que te sientas así! Identifica qué contribuye a tu bienestar y sigue cultivándolo. 🌻",
        "calma": "Disfruta este momento de tranquilidad y procura mantener hábitos que favorezcan tu bienestar. 🌿",
        "confusion": "Aunque tengas dudas, puedes confiar en tus recursos y avanzar paso a paso. 💙"
    }

    return consejos.get(
        emocion,
        "¡Gracias por compartir tu bienestar! Sigue cuidando de ti. 💙"
    )


@app.route("/", methods=["GET", "POST"])
@login_required
def inicio():
    mensaje = None
    consejo = None

    if request.method == "POST":

            try:
                puntuacion = int(request.form["puntuacion"])
                emocion = request.form["emocion"]

                emociones_validas = {
                    "alegria", "tristeza", "estres", "enojo",
                    "miedo", "calma", "confusion"
                }

                if puntuacion not in range(1, 6):
                    raise ValueError("Puntuación no válida")

                if emocion not in emociones_validas:
                    raise ValueError("Emoción no válida")

                hoy = date.today()

                registro = RegistroBienestar.query.filter_by(
                    fecha=hoy,
                    usuario_id=current_user.id
                ).first()

                if registro is None:
                    registro = RegistroBienestar(
                        fecha=hoy,
                        puntuacion=puntuacion,
                        emocion=emocion,
                        usuario_id=current_user.id
                    )
                    db.session.add(registro)
                else:
                    registro.puntuacion = puntuacion
                    registro.emocion = emocion

                db.session.commit()

                mensaje = "¡Tu registro se guardó correctamente!"
                consejo = obtener_consejo(puntuacion, emocion)

            except (ValueError, KeyError):
                db.session.rollback()
                mensaje = "No pudimos guardar el registro."
                consejo = "Selecciona una puntuación y una emoción válidas."

    registros = RegistroBienestar.query.filter_by(
        usuario_id=current_user.id
    ).order_by(
        RegistroBienestar.fecha.desc()
    ).limit(7).all()

    return render_template_string(
        PAGINA,
        mensaje=mensaje,
        consejo=consejo,
        registros=registros
    )

if __name__ == "__main__":
    app.run(debug=True)
