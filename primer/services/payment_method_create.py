import uuid

from primer.payment_processors import PaymentProcessors
from primer.exceptions import InvalidPaymentMethod, InvalidCustomer
from primer.models.customer import Customer
from primer.models.payment_processor_customer_information import PaymentProcessorCustomerInformation
from primer.models.payment_method import PaymentMethod
from primer.models.payment_processor_payment_information import PaymentProcessorPaymentInformation
from primer.services.payment_processor_payment_information_create import PaymentProcessorPaymentInformationCreate

class PaymentMethodCreate:
    MANDATORY_FIELDS = [
        'cardholder_name',
        'number',
        'cvv',
        'expiration_date'
    ]

    def __init__(self, processor_name: str, customer_token: str, payment_token: str, details: dict):
        self._find_customer(customer_token)
        self.payment_token = payment_token
        self.processor_name = processor_name
        self.processor = PaymentProcessors(processor_name)
        self.details = self._slice(details)

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

            payment_information = PaymentProcessorPaymentInformationCreate.call(
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

    def _slice(self, details: dict) -> dict:
        sliced_details = {}

        for k in PaymentMethodCreate.MANDATORY_FIELDS:
            if details.get(k) is not None:
                sliced_details[k] = details[k]
            else:
                raise InvalidPaymentMethod


        return sliced_details

    @classmethod
    def call(kls, processor_name: str, customer_token: str, payment_token: str, details: dict):
        service = kls(processor_name, customer_token, payment_token, details)

        payment_method = service.create_payment_method()

        service.create_payment_processor_payment_information(payment_method)

        return payment_method







