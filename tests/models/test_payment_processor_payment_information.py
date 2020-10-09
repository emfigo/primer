import pytest
import uuid

from primer import db
from primer.models.customer import Customer
from primer.models.payment_method import PaymentMethod
from primer.models.payment_processor_payment_information import PaymentProcessorPaymentInformation

@pytest.mark.usefixtures('database')
class TestPaymentProcessorPaymentInformation:
    details = {
        'card_holder_name': 'Test Coool',
        'number': '1111' * 4,
        'cvv': '111',
        'expiration_date': '12/99'
    }

    def test_creates_customer_with_all_expected_attributes(self, database):
        name = 'braintreetest'
        information = {
            'payment_token': 'sometoken',
            'nonce_token': 'someothertoken'
        }

        customer = Customer.create(
            first_name = 'Test',
            last_name = 'Test',
            company = 'Really Cool LTD',
            email = 'test.test@reallycool.test',
            phone = '+1111111111',
            fax = '+12222222222',
            website = 'https://www.reallycool.test'
        )

        payment_method = PaymentMethod.create(
            customer = customer,
            details = self.details,
        )

        payment_processor_payment_information =  PaymentProcessorPaymentInformation.create(
            name = name,
            payment_method = payment_method,
            information = information
        )

        assert PaymentProcessorPaymentInformation.query.filter_by(
            name = name
        ).first().id == payment_processor_payment_information.id

        assert payment_processor_payment_information.id is not None

        assert payment_processor_payment_information.name == name
        assert payment_processor_payment_information.information == information
        assert payment_processor_payment_information.payment_method_id == payment_method.id

    def test_find_by_id_retrieves_the_expected_payment_processor_payment_information(self, database):
        name = 'stripetest'
        information = {
            'payment_token': 'sometoken'
        }

        customer = Customer.create(
            first_name = 'Test',
            last_name = 'Test',
            company = 'Really Cool LTD',
            email = 'test.test@reallycool.test',
            phone = '+1111111111',
            fax = '+12222222222',
            website = 'https://www.reallycool.test'
        )

        payment_method = PaymentMethod.create(
            customer = customer,
            details = self.details,
        )

        payment_processor_payment_information =  PaymentProcessorPaymentInformation.create(
            name = name,
            payment_method = payment_method,
            information = information
        )

        assert PaymentProcessorPaymentInformation.find_by_id(uuid.uuid4()) is None
        assert PaymentProcessorPaymentInformation.find_by_id(payment_processor_payment_information.id) is not None
        assert PaymentProcessorPaymentInformation.find_by_id(payment_processor_payment_information.id) == payment_processor_payment_information

