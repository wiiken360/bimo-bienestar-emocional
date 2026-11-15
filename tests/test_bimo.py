
import os

# Activar el modo de pruebas antes de importar la aplicación.
os.environ["BIMO_TESTING"] = "1"

import pytest

from app import app, db, Usuario, Organizacion, obtener_consejo
from werkzeug.security import generate_password_hash

# Base de datos temporal en memoria.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["TESTING"] = True

@pytest.fixture()
def cliente():
    with app.app_context():
        db.create_all()

        organizacion = Organizacion(
            nombre="Organizacion de Prueba",
            activa=True
        )
        db.session.add(organizacion)
        db.session.commit()

        usuario = Usuario(
            nombre="Trabajador de Prueba",
            correo="trabajador@test.cl",
            contrasena_hash=generate_password_hash("Prueba12345"),
            rol="trabajador",
            organizacion_id=organizacion.id,
            activo=True
        )
        db.session.add(usuario)
        db.session.commit()
        usuario_organizacional = Usuario(
            nombre="Encargado Organizacional",
            correo="organizacion@test.cl",
            contrasena_hash=generate_password_hash("OrgPrueba123"),
            rol="organizacional",
            organizacion_id=organizacion.id,
            activo=True
        )

        db.session.add(usuario_organizacional)
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()

def test_consejo_estres_bienestar_bajo():
    consejo = obtener_consejo(2, "estres")

    assert "pausa" in consejo.lower()
    assert "respirar" in consejo.lower()


def test_consejo_tristeza_bienestar_bajo():
    consejo = obtener_consejo(2, "tristeza")

    assert "confianza" in consejo.lower()
    assert "conversar" in consejo.lower()


def test_emociones_generan_consejos_diferentes():
    consejo_estres = obtener_consejo(2, "estres")
    consejo_tristeza = obtener_consejo(2, "tristeza")

    assert consejo_estres != consejo_tristeza


def test_consejo_bienestar_intermedio():
    consejo = obtener_consejo(3, "alegria")

    assert "alegría" in consejo.lower()

def test_trabajador_puede_iniciar_sesion(cliente):
    respuesta = cliente.post(
        "/login",
        data={
            "correo": "trabajador@test.cl",
            "contrasena": "Prueba12345"
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200
    assert b"Mis registros recientes" in respuesta.data
def test_trabajador_no_puede_acceder_al_panel_admin(cliente):
    cliente.post(
        "/login",
        data={
            "correo": "trabajador@test.cl",
            "contrasena": "Prueba12345"
        }
    )

    respuesta = cliente.get("/admin")

    assert respuesta.status_code == 403

def test_usuario_organizacional_puede_acceder_a_su_panel(cliente):
    respuesta = cliente.post(
        "/login",
        data={
            "correo": "organizacion@test.cl",
            "contrasena": "OrgPrueba123"
        },
        follow_redirects=True
    )

    assert respuesta.status_code == 200, respuesta.data.decode("utf-8")



def test_usuario_organizacional_no_puede_acceder_al_panel_admin(cliente):
    cliente.post(
        "/login",
        data={
            "correo": "organizacion@test.cl",
            "contrasena": "OrgPrueba123"
        }
    )

    respuesta = cliente.get("/admin")

    assert respuesta.status_code == 403