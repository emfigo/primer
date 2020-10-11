import pytest

from primer.models.customer import Customer
from primer.models.payment_method import PaymentMethod
from primer.models.payment_processor_customer_information import PaymentProcessorCustomerInformation
from primer.models.payment_processor_payment_information import PaymentProcessorPaymentInformation
from primer.services.payment_method_create import PaymentMethodCreate

@pytest.mark.usefixtures('database', 'payment_processors')
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

    customer_information = {
        'customer_id': 'someid'
    }

    payment_details = {
        'card_holder_name': 'Test Coool',
        'number': '1111' * 4,
        'cvv': '111',
        'expiration_date': '12/99'
    }

    processor_name = 'someprocessor'

    def test_creates_payment_method_when_all_details_valid_and_does_not_exist(self, database, payment_processors):
        customer = Customer.create(**self.customer_details)
        PaymentProcessorCustomerInformation.create(
            name = self.processor_name,
            customer = customer,
            information = self.customer_information
        )

        before_count = PaymentMethod.query.count()

        payment_method = PaymentMethodCreate.call(self.processor_name, customer.token, None, self.payment_details)

        assert PaymentMethod.query.count() == before_count + 1

        assert payment_method.customer_id == customer.id
        assert payment_method.details == self.payment_details

        payment_information = PaymentProcessorPaymentInformation.find_by_payment_method_id_and_processor_name(payment_method.id, self.processor_name)

        assert payment_information.information == { 'payment_token': 'sometoken', 'nonce_token': 'sometoken' }

    def test_returns_existing_payment_method_when_token_provided(self, database, payment_processors):
        customer = Customer.create(**self.customer_details)
        PaymentProcessorCustomerInformation.create(
            name = self.processor_name,
            customer = customer,
            information = self.customer_information
        )

        prev_payment_method = PaymentMethodCreate.call(self.processor_name, customer.token, None, self.payment_details)
        prev_payment_information = PaymentProcessorPaymentInformation.find_by_payment_method_id_and_processor_name(prev_payment_method.id, self.processor_name)

        before_count_payment_method = PaymentMethod.query.count()
        before_count_payment_information = PaymentProcessorPaymentInformation.query.count()

        payment_method = PaymentMethodCreate.call(self.processor_name, customer.token, prev_payment_method.token, self.payment_details)
        payment_information = PaymentProcessorPaymentInformation.find_by_payment_method_id_and_processor_name(payment_method.id, self.processor_name)

        assert PaymentMethod.query.count() == before_count_payment_method
        assert PaymentProcessorPaymentInformation.query.count() == before_count_payment_information

        assert prev_payment_method.id == payment_method.id
        assert prev_payment_information.id == payment_information.id

