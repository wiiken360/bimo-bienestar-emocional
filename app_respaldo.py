from flask import Flask, render_template_string

app = Flask(__name__)

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
            padding: 40px 20px;
        }
        .tarjeta {
            background: white;
            max-width: 480px;
            margin: 30px auto;
            padding: 30px;
            border-radius: 24px;
            box-shadow: 0 8px 25px #cbd7e8;
        }
        .mascota {
            font-size: 100px;
        }
        button {
            background: #6387e8;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 18px;
            margin: 6px;
            cursor: pointer;
            font-size: 15px;
        }
        button:hover {
            background: #4568c5;
        }
        #respuesta {
            margin-top: 24px;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <h1>Mi espacio emocional</h1>

    <div class="tarjeta">
        <div class="mascota">🐻</div>
        <h2>¡Hola! Soy Bimo</h2>
        <p>Estoy aquí para acompañarte.</p>
        <p><strong>¿Cómo te sientes hoy?</strong></p>

        <button onclick="sentir('feliz')">😊 Feliz</button>
        <button onclick="sentir('triste')">😔 Triste</button>
        <button onclick="sentir('estresado')">😣 Estresado</button>

        <div id="respuesta"></div>
    </div>

    <script>
        function sentir(emocion) {
            const mensajes = {
                feliz: "¡Qué bueno! Disfruta este momento y reconoce lo que te hace bien. 💙",
                triste: "Está bien sentirse triste. Puedes darte un momento para reconocer lo que sientes. 💙",
                estresado: "Hagamos una pausa. Respira lentamente y date unos momentos de tranquilidad. 🌿"
            };

            document.getElementById("respuesta").innerText =
                mensajes[emocion];
        }
    </script>
</body>
</html>
"""

@app.route("/")
def inicio():
    return render_template_string(PAGINA)

if __name__ == "__main__":
    app.run(debug=True)