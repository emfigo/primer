from flask import Response
from flask.testing import FlaskClient
import json
import pytest
from unittest import mock

from primer import app, db
from primer.blueprints.customers import customers
from primer.blueprints.payment_methods import payment_methods
from primer.blueprints.sales import sales
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
    app.register_blueprint(payment_methods)
    app.register_blueprint(sales)
    return app

@pytest.fixture(scope='session')
def payment_processors():
    mock_customer = mock.MagicMock(name='customer')
    mock_customer.is_success = True
    mock_customer.customer.id = 'someid'

    mock_sale = mock.MagicMock(name='sale')
    mock_sale.is_success = True

    mock_payment_method = mock.MagicMock(name='payment_method')
    mock_payment_method.is_success = True
    mock_payment_method.credit_card.token = 'sometoken'

    mock_payment_method_nonce = mock.MagicMock(name='payment_method_nonce')
    mock_payment_method_nonce.is_success = True
    mock_payment_method_nonce.payment_method_nonce.nonce = 'sometoken'

    mock_processor = mock.MagicMock(name='processor')
    mock_processor.customer.create.return_value = mock_customer
    mock_processor.credit_card.create.return_value = mock_payment_method
    mock_processor.payment_method_nonce.create.return_value = mock_payment_method_nonce
    mock_processor.transaction.sale.return_value = mock_sale

    new_paymentprocessors = mock.MagicMock(name='processors')
    new_paymentprocessors.get.return_value = mock_processor

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

