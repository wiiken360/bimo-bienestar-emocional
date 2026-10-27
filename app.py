
from datetime import date
import os

from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuracion de la base de datos
os.makedirs(app.instance_path, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bimo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Modelo inicial de los registros de bienestar
class RegistroBienestar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, unique=True)
    puntuacion = db.Column(db.Integer, nullable=False)
    emocion = db.Column(db.String(30), nullable=False)


# Crear las tablas si todavia no existen
with app.app_context():
    db.create_all()


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
            Prototipo local: estos datos todavía no están asociados
            a una cuenta personal.
        </p>
    </div>
</body>
</html>
"""


def obtener_consejo(puntuacion, emocion):
    if puntuacion <= 2:
        return (
            "Gracias por compartir cómo te sientes. "
            "Puedes darte una pausa y considerar buscar apoyo "
            "si sientes que lo necesitas. 💙"
        )

    if puntuacion == 3:
        return (
            "Gracias por registrar tu bienestar. "
            "¿Qué pequeña acción podría ayudarte hoy? 🌿"
        )

    return (
        "¡Gracias por compartir tu registro! "
        "Reconoce aquello que está contribuyendo a tu bienestar. 💙"
    )


@app.route("/", methods=["GET", "POST"])
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

            # Prototipo de un solo usuario:
            # actualiza el registro del día si ya existe.
            registro = RegistroBienestar.query.filter_by(
                fecha=hoy
            ).first()

            if registro is None:
                registro = RegistroBienestar(
                    fecha=hoy,
                    puntuacion=puntuacion,
                    emocion=emocion
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

    registros = RegistroBienestar.query.order_by(
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
