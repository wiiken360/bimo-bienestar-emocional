from getpass import getpass

from app import app, db, Usuario
from werkzeug.security import generate_password_hash


with app.app_context():

    print("\n=== CREAR ADMINISTRADOR BIMО ===")

    nombre = input("Nombre del administrador: ").strip()
    correo = input("Correo electrónico: ").strip().lower()

    if not nombre or not correo:
        print("Error: debes ingresar nombre y correo.")
    elif Usuario.query.filter_by(correo=correo).first():
        print("Ya existe un usuario con ese correo.")
    else:
        contrasena = getpass("Crear contraseña: ")
        confirmacion = getpass("Confirmar contraseña: ")

        if len(contrasena) < 10:
            print("La contraseña debe tener al menos 10 caracteres.")

        elif contrasena != confirmacion:
            print("Las contraseñas no coinciden.")

        else:
            administrador = Usuario(
                nombre=nombre,
                correo=correo,
                contrasena_hash=generate_password_hash(contrasena),
                rol="administrador",
                organizacion_id=None,
                activo=True
            )

            db.session.add(administrador)
            db.session.commit()

            print("\n¡Administrador creado correctamente!")
            print("Correo:", correo)
            print("Rol: administrador")