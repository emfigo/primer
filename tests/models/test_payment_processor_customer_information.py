import pytest
import uuid

from primer import db
from primer.exceptions import InvalidCustomer
from primer.models.customer import Customer
from primer.models.payment_processor_customer_information import PaymentProcessorCustomerInformation

@pytest.mark.usefixtures('database')
class TestPaymentProcessorCustomerInformation:
    def test_creates_payment_processor_customer_information_with_all_expected_attributes(self, database):
        name = 'braintreetest'
        information = {
            'customer_id': 'someid'
        }

        customer = Customer.create(
            first_name='Test',
            last_name='Coool',
            company='Really Cool LTD',
            email='test.coool@reallycool.test',
            phone='+1111111111',
            fax='+12222222222',
            website='https://www.reallycool.test'
        )

        payment_processor_customer_information =  PaymentProcessorCustomerInformation.create(
            name = name,
            customer = customer,
            information = information
        )

        assert PaymentProcessorCustomerInformation.query.filter_by(
            name = name
        ).first().id == payment_processor_customer_information.id

        assert payment_processor_customer_information.id is not None

        assert payment_processor_customer_information.name == name
        assert payment_processor_customer_information.information == information

    def test_does_not_creates_payment_processor_customer_information_with_invalid_customer(self, database):
        name = 'braintreetest'
        information = {
            'customer_id': 'someid'
        }

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

        with pytest.raises(InvalidCustomer):
            PaymentProcessorCustomerInformation.create(
                name = name,
                customer = customer,
                information = information
            )

        assert PaymentProcessorCustomerInformation.query.filter_by(
            customer_id = customer.id
        ).first() is None


    def test_find_by_id_retrieves_the_expected_payment_processor_customer_information(self, database):
        name = 'stripetest'
        information = {
            'payment_token': 'sometoken',
            'customer_id': 'someid'
        }

        customer = Customer.create(
            first_name='Test',
            last_name='Coool',
            company='Really Cool LTD',
            email='test.coool@reallycool.test',
            phone='+1111111111',
            fax='+12222222222',
            website='https://www.reallycool.test'
        )

        payment_processor_customer_information =  PaymentProcessorCustomerInformation.create(
            name = name,
            customer = customer,
            information = information
        )

        assert PaymentProcessorCustomerInformation.find_by_id(uuid.uuid4()) is None
        assert PaymentProcessorCustomerInformation.find_by_id(payment_processor_customer_information.id) is not None
        assert PaymentProcessorCustomerInformation.find_by_id(payment_processor_customer_information.id) == payment_processor_customer_information


    def test_find_by_customer_id_retrieves_the_expected_payment_processor_customer_information(self, database):
        name = 'stripetest'
        information = {
            'payment_token': 'sometoken',
            'customer_id': 'someid'
        }

        customer = Customer.create(
            first_name='Test',
            last_name='Coool',
            company='Really Cool LTD',
            email='test.coool@reallycool.test',
            phone='+1111111111',
            fax='+12222222222',
            website='https://www.reallycool.test'
        )

        payment_processor_customer_information =  PaymentProcessorCustomerInformation.create(
            name = name,
            customer = customer,
            information = information
        )

        assert PaymentProcessorCustomerInformation.find_by_customer_id(uuid.uuid4()) is None
        assert PaymentProcessorCustomerInformation.find_by_customer_id(customer.id) is not None
        assert PaymentProcessorCustomerInformation.find_by_customer_id(customer.id) == payment_processor_customer_information
