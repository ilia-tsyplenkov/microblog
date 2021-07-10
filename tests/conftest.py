import sys
import os
import pytest
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from config import Config
from app import create_app, db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


@pytest.fixture(scope='function', autouse=True)
def prepare_db(request):
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    def delete_db():
        db.session.remove()
        db.drop_all()
        app_context.pop()
    request.addfinalizer(delete_db)
    return app
