import pytest
import uuid
from unittest import mock

from primer.models.customer import Customer
from primer.models.payment_processor_customer_information import PaymentProcessorCustomerInformation
from primer.services.payment_processor_customer_information_create import PaymentProcessorCustomerInformationCreate

@pytest.mark.usefixtures('database')
class TestCustomerCreate:
    customer_details = {
        'first_name': 'Interesting',
        'last_name': 'Test',
        'company': 'Really Interesting LTD',
        'email': 'interesting.test1@reallyinteresting.test',
        'phone': '+1111111111',
        'fax': '+12222222222',
        'website': 'https://www.reallyinteresting.test'
    }

    processor_name = 'someprocessor'

    payment_processor_customer_information = {
        'customer_id': 'someid'
    }


    def test_creates_payment_processor_customer_information_when_all_details_correct(self, database):
        customer = Customer.create(**self.customer_details)

        before_count = PaymentProcessorCustomerInformation.query.count()

        payment_processor_customer_information = PaymentProcessorCustomerInformationCreate.call(
            self.processor_name,
            customer,
            self.payment_processor_customer_information
        )

        assert PaymentProcessorCustomerInformation.query.count() == before_count + 1
        assert payment_processor_customer_information.name == self.processor_name
        assert payment_processor_customer_information.customer_id == customer.id
        assert payment_processor_customer_information.information == self.payment_processor_customer_information

    def test_returns_existing_payment_processor_customer_information_when_customer_exists(self, database):
        customer = Customer.create(**self.customer_details)

        prev_payment_processor_customer_information = PaymentProcessorCustomerInformationCreate.call(
            self.processor_name,
            customer,
            self.payment_processor_customer_information
        )

        before_count = PaymentProcessorCustomerInformation.query.count()

        payment_processor_customer_information = PaymentProcessorCustomerInformationCreate.call(
            self.processor_name,
            customer,
            self.payment_processor_customer_information
        )

        assert PaymentProcessorCustomerInformation.query.count() == before_count
        assert payment_processor_customer_information.id == prev_payment_processor_customer_information.id
