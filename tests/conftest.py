import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import pytest

from app import app, db

@pytest.fixture(scope='session', autouse=True)
def prepare_db(request):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    db.create_all()
    def delete_db():
        db.session.remove()
        db.drop_all()
    request.addfinalizer(delete_db)
    return db
