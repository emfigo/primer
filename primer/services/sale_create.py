from primer.exceptions import InvalidCustomer, InvalidPaymentMethod
from primer.models.customer import Customer
from primer.models.payment_method import PaymentMethod
from primer.models.payment_processor_payment_information import PaymentProcessorPaymentInformation
from primer.services import utils
from primer.payment_processors import PaymentProcessors

class SaleCreate:
    MANDATORY_FIELDS = [
        'amount'
    ]

    OPTIONAL_FIELDS = []

    def __init__(self, processor_name: str, customer_token: str, payment_token: str, details: dict):
        self._find_customer(customer_token)
        self._find_payment_method(payment_token)
        self.processor_name = processor_name
        self.processor = PaymentProcessors(processor_name)
        self.details = utils.slice(SaleCreate, details)

    def _find_customer(self, token: str):
        self.customer = Customer.find_by_token(token)

        if self.customer is None:
            raise InvalidCustomer

    def _find_payment_method(self, token: str):
        self.payment_method = PaymentMethod.find_by_token(token)

        if self.payment_method is None:
            raise InvalidPaymentMethod

    def create_sale(self):
        payment_processor_payment_information = PaymentProcessorPaymentInformation.find_by_payment_method_id_and_processor_name(self.payment_method.id, self.processor_name)

        payment_method_nonce_info = self.processor.create_payment_method_nonce(payment_processor_payment_information.information)

        return self.processor.create_sale({**self.details, **payment_method_nonce_info})


    @classmethod
    def call(kls, processor_name: str, customer_token: str, payment_token: str, details: dict):
        output = {}
        service = kls(processor_name, customer_token, payment_token, details)

        if service.create_sale():
            output['message'] = f"transaction was made successfully for amount {details['amount']}"

        return output
