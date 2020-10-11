from flask import Response
from flask.testing import FlaskClient
import json
import pytest
from unittest import mock

from primer import app, db
from primer.blueprints.customers import customers
from primer.payment_processors import PaymentProcessors


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

@pytest.fixture(scope='session')
def payment_processors():
    new_paymentprocessors = mock.MagicMock()

    with mock.patch('primer.payment_processors.PaymentProcessors.PAYMENT_GATEWAYS', new_paymentprocessors) as payment_processors:
        yield payment_processors


class MyResponse(Response):
    """Implements custom deserialisation method for response objects"""

    @property
    def text(self):
        return self.get_data(as_text=True)

    @property
    def json(self):
        return json.loads(self.text)

