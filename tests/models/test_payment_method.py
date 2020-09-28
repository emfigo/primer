
import pytest
import uuid

from primer import db
from primer.exceptions import InvalidCustomer, InvalidPaymentProcessorInformation
from primer.models.customer import Customer
from primer.models.payment_processor_information import PaymentProcessorInformation
from primer.models.payment_method import PaymentMethod

@pytest.mark.usefixtures('database')
class TestPaymentMethod:
    def test_creates_payment_method_with_all_attributes_correct(self, database):
        customer = Customer.create(
            first_name='Test',
            last_name='Coool',
            company='Really Cool LTD',
            email='test.coool@reallycool.test',
            phone='+1111111111',
            fax='+12222222222',
            website='https://www.reallycool.test'
        )

        payment_processor_information =  PaymentProcessorInformation.create(
            name = 'braintree',
            information = {
                'payment_token': 'sometoken',
                'nonce_token': 'someothertoken',
                'customer_id': 'someid'
            }
        )

        details = {
            'card_holder_name': 'Test Coool',
            'number': '1111' * 4,
            'cvv': '111',
            'expiration_date': '12/99'
        }

        payment_method = PaymentMethod.create(
            customer = customer,
            details = details,
            payment_processor_information = payment_processor_information
        )

        assert PaymentMethod.query.filter_by(
            customer_id = customer.id
        ).first().id == payment_method.id

        assert payment_method.id is not None

        assert PaymentMethod.query.filter_by(
            customer_id = customer.id
        ).first().token == payment_method.token

        assert payment_method.token is not None

        assert payment_method.customer_id == customer.id
        assert payment_method.details == details
        assert payment_method.payment_processor_information_id == payment_processor_information.id

    def test_does_not_create_payment_method_with_invalid_customer(self, database):
        customer = Customer(
            id = uuid.uuid4(),
            first_name='None',
            last_name='Existing',
            company='Really Cool LTD',
            email='exception.lover@reallycool.test',
            phone='+1111111111',
            fax='+12222222222',
            website='https://www.reallycool.test'
        )

        payment_processor_information =  PaymentProcessorInformation.create(
            name = 'braintree',
            information = {
                'payment_token': 'sometoken',
                'nonce_token': 'someothertoken',
                'customer_id': 'someid'
            }
        )

        details = {
            'card_holder_name': 'Test Coool',
            'number': '1111' * 4,
            'cvv': '111',
            'expiration_date': '12/99'
        }

        with pytest.raises(InvalidCustomer):
            payment_method = PaymentMethod.create(
                customer = customer,
                details = details,
                payment_processor_information = payment_processor_information
            )

        assert PaymentMethod.query.filter_by(
            customer_id = customer.id
        ).first() is None

    def test_does_not_create_payment_method_with_invalid_payment_processor_information(self, database):
        customer = Customer.create(
            first_name='Exception',
            last_name='Another',
            company='Really Cool LTD',
            email='exception.lover2@reallycool.test',
            phone='+1111111111',
            fax='+12222222222',
            website='https://www.reallycool.test'
        )

        payment_processor_information =  PaymentProcessorInformation(
            id = uuid.uuid4(),
            name = 'braintree',
            information = {
                'payment_token': 'sometoken',
                'nonce_token': 'someothertoken',
                'customer_id': 'someid'
            }
        )

        details = {
            'card_holder_name': 'Test Coool',
            'number': '1111' * 4,
            'cvv': '111',
            'expiration_date': '12/99'
        }

        with pytest.raises(InvalidPaymentProcessorInformation):
            payment_method = PaymentMethod.create(
                customer = customer,
                details = details,
                payment_processor_information = payment_processor_information
            )

        assert PaymentMethod.query.filter_by(
            customer_id = customer.id
        ).first() is None

    def test_find_by_id_retrieves_the_expected_payment_method(self, database):
        customer = Customer.create(
            first_name='Test',
            last_name='Coool2',
            company='Really Cool LTD',
            email='test.coool2@reallycool.test',
            phone='+1111111111',
            fax='+12222222222',
            website='https://www.reallycool.test'
        )

        payment_processor_information =  PaymentProcessorInformation.create(
            name = 'braintree',
            information = {
                'payment_token': 'sometoken',
                'nonce_token': 'someothertoken',
                'customer_id': 'someid'
            }
        )

        details = {
            'card_holder_name': 'Test Coool',
            'number': '1111' * 4,
            'cvv': '111',
            'expiration_date': '12/99'
        }

        payment_method = PaymentMethod.create(
            customer = customer,
            details = details,
            payment_processor_information = payment_processor_information
        )

        assert PaymentMethod.find_by_id(uuid.uuid4()) is None
        assert PaymentMethod.find_by_id(payment_method.id) is not None
        assert PaymentMethod.find_by_id(payment_method.id) == payment_method

    def test_find_by_token_retrieves_the_expected_payment_method(self, database):
        customer = Customer.create(
            first_name='Test',
            last_name='Coool3',
            company='Really Cool LTD',
            email='test.coool3@reallycool.test',
            phone='+1111111111',
            fax='+12222222222',
            website='https://www.reallycool.test'
        )

        payment_processor_information =  PaymentProcessorInformation.create(
            name = 'braintree',
            information = {
                'payment_token': 'sometoken',
                'nonce_token': 'someothertoken',
                'customer_id': 'someid'
            }
        )

        details = {
            'card_holder_name': 'Test Coool',
            'number': '1111' * 4,
            'cvv': '111',
            'expiration_date': '12/99'
        }

        payment_method = PaymentMethod.create(
            customer = customer,
            details = details,
            payment_processor_information = payment_processor_information
        )

        assert PaymentMethod.find_by_token('nonexistingtoken') is None
        assert PaymentMethod.find_by_token(payment_method.token) is not None
        assert PaymentMethod.find_by_token(payment_method.token) == payment_method
