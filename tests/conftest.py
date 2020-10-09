from flask import Response
from flask.testing import FlaskClient
import json
import pytest

from primer import app, db
from primer.blueprints.customers import customers


@pytest.fixture(scope='function')
def database(request):
    db.create_all()

    yield db

    @request.addfinalizer
    def drop_database():
        try:
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())

            db.session.commit()
        finally:
            db.session.rollback()

@pytest.fixture(scope='session')
def testapp():
    app.config['TESTING'] = True
    app.response_class = MyResponse
    app.test_client_class = FlaskClient

    app.register_blueprint(customers)
    return app

class MyResponse(Response):
    """Implements custom deserialisation method for response objects"""

    @property
    def text(self):
        return self.get_data(as_text=True)

    @property
    def json(self):
        return json.loads(self.text)
