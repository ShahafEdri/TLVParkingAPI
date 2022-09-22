import os
import tempfile

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flaskr import create_app
from flaskr.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client: FlaskClient):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client: FlaskClient):
    return AuthActions(client)


@pytest.fixture
def parking_lots():
    return {
        "123": {
            "parking_id": "123",
            "name_hebrew": "חניון ארלוזורוב 17",
            "name_english": None,
            "address_hebrew": "ארלוזורוב 17 תל-אביב יפו",
            "address_english": None,
            "geo_lat": None,
            "geo_lng": None
        },
        "3": {
            "parking_id": "3",
            "name_hebrew": "חניון בזל",
            "name_english": None,
            "address_hebrew": "אשתורי הפרחי 5 תל-אביב יפו",
            "address_english": None,
            "geo_lat": None,
            "geo_lng": None
        },
        "45": {
            "parking_id": "45",
            "name_hebrew": "חניון תל-נורדאו",
            "name_english": None,
            "address_hebrew": "פרישמן 28 תל-אביב יפו",
            "address_english": None,
            "geo_lat": None,
            "geo_lng": None
        },
    }


@pytest.fixture
def tonnage_legitimate_values():
    return ['full', 'almost full', 'available', 'closed', 'not_valid']
