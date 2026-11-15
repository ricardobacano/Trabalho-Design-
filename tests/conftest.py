import pytest

from app import create_app
from app.banco import db


@pytest.fixture()
def app():
    aplicativo = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "teste",
            "NOTIFICADOR_FALHAR": False,
        }
    )
    yield aplicativo
    with aplicativo.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
