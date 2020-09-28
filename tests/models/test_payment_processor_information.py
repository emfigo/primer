import pytest
import uuid

from primer import db
from primer.models.payment_processor_information import PaymentProcessorInformation

@pytest.mark.usefixtures('database')
class TestPaymentProcessorInformation:
    def test_creates_customer_with_all_expected_attributes(self, database):
        name = 'braintreetest'
        information = {
            'payment_token': 'sometoken',
            'nonce_token': 'someothertoken',
            'customer_id': 'someid'
        }

        payment_processor_information =  PaymentProcessorInformation.create(
            name = name,
            information = information
        )

        assert PaymentProcessorInformation.query.filter_by(
            name = name
        ).first().id == payment_processor_information.id

        assert payment_processor_information.id is not None

        assert payment_processor_information.name == name
        assert payment_processor_information.information == information

    def test_find_by_retrieves_teh_expected_payment_processor_information(self, database):
        name = 'stripetest'
        information = {
            'payment_token': 'sometoken',
            'customer_id': 'someid'
        }

        payment_processor_information =  PaymentProcessorInformation.create(
            name = name,
            information = information
        )

        assert PaymentProcessorInformation.find_by_id(uuid.uuid4()) is None
        assert PaymentProcessorInformation.find_by_id(payment_processor_information.id) is not None
        assert PaymentProcessorInformation.find_by_id(payment_processor_information.id) == payment_processor_information

