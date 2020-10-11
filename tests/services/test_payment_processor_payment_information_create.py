import pytest

from primer.models.customer import Customer
from primer.models.payment_method import PaymentMethod
from primer.models.payment_processor_payment_information import PaymentProcessorPaymentInformation
from primer.services.payment_processor_payment_information_create import PaymentProcessorCustomerInformationCreate

@pytest.mark.usefixtures('database')
class TestPaymentProcessorPaymentInformationCreate:
    customer_details = {
        'first_name': 'Interesting',
        'last_name': 'Test',
        'company': 'Really Interesting LTD',
        'email': 'interesting.test1@reallyinteresting.test',
        'phone': '+1111111111',
        'fax': '+12222222222',
        'website': 'https://www.reallyinteresting.test'
    }

    payment_details = {
        'card_holder_name': 'Test Coool',
        'number': '1111' * 4,
        'cvv': '111',
        'expiration_date': '12/99'
    }

    processor_name = 'someprocessor'

    payment_processor_payment_information = {
        'payment_token': 'sometoken',
        'nonce_token': 'someothertoken'
    }


    def test_creates_payment_processor_customer_information_when_all_details_correct(self, database):
        customer = Customer.create(**self.customer_details)
        payment_method = PaymentMethod.create(customer, self.payment_details)

        before_count = PaymentProcessorPaymentInformation.query.count()

        payment_processor_payment_information = PaymentProcessorCustomerInformationCreate.call(
            self.processor_name,
            payment_method,
            self.payment_processor_payment_information
        )

        assert PaymentMethod.query.count() == before_count + 1
        assert payment_processor_payment_information.name == self.processor_name
        assert payment_processor_payment_information.payment_method_id == payment_method.id
        assert payment_processor_payment_information.information == self.payment_processor_payment_information

    def test_returns_existing_payment_processor_payment_information_when_payment_method_exists(self, database):
        customer = Customer.create(**self.customer_details)
        payment_method = PaymentMethod.create(customer, self.payment_details)

        prev_payment_processor_payment_information = PaymentProcessorCustomerInformationCreate.call(
            self.processor_name,
            payment_method,
            self.payment_processor_payment_information
        )

        before_count = PaymentProcessorPaymentInformation.query.count()

        payment_processor_payment_information = PaymentProcessorCustomerInformationCreate.call(
            self.processor_name,
            payment_method,
            self.payment_processor_payment_information
        )

        assert PaymentProcessorPaymentInformation.query.count() == before_count
        assert payment_processor_payment_information.id == prev_payment_processor_payment_information.id

