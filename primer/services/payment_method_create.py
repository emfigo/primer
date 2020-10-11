import uuid

from primer.payment_processors import PaymentProcessors
from primer.exceptions import InvalidPaymentProcessorPaymentInformation, InvalidCustomer
from primer.models.customer import Customer
from primer.models.payment_processor_customer_information import PaymentProcessorCustomerInformation
from primer.models.payment_method import PaymentMethod
from primer.models.payment_processor_payment_information import PaymentProcessorPaymentInformation
from primer.services.payment_processor_payment_information_create import PaymentProcessorCustomerInformationCreate

class PaymentMethodCreate:
    def __init__(self, processor_name: str, customer_token: str, payment_token: str, details: dict):
        self._find_customer(customer_token)
        self.payment_token = payment_token
        self.processor_name = processor_name
        self.processor = PaymentProcessors(processor_name)
        self.details = details

    def _find_customer(self, token: str):
        self.customer = Customer.find_by_token(token)

        if self.customer is None:
            raise InvalidCustomer


    def create_payment_processor_payment_information(self, payment_method):
        payment_information = PaymentProcessorPaymentInformation.find_by_payment_method_id_and_processor_name(
            payment_method.id,
            self.processor_name
        )

        if payment_information is None:
            customer_information = PaymentProcessorCustomerInformation.find_by_customer_id_and_processor_name(
                self.customer.id,
                self.processor_name
            )

            payment_information = self.processor.create_payment_method(
                { **customer_information.information, **self.details }
            )

            payment_information = PaymentProcessorCustomerInformationCreate.call(
                self.processor_name,
                payment_method,
                payment_information
            )

        return payment_information


    def create_payment_method(self):
        payment_method = PaymentMethod.find_by_token(self.payment_token)

        if payment_method is None:
            payment_method = PaymentMethod.create(self.customer, self.details)

        return payment_method

    @classmethod
    def call(kls, processor_name: str, customer_token: str, payment_token: str, details: dict):
        service = kls(processor_name, customer_token, payment_token, details)

        payment_method = service.create_payment_method()

        service.create_payment_processor_payment_information(payment_method)

        return payment_method







