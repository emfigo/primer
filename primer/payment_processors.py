import braintree

from config import BRAINTREE_CONFIG
from primer.exceptions import InvalidPaymentProcessorPaymentInformation, InvalidPaymentProcessorCustomerInformation

class PaymentProcessors:
    PAYMENT_GATEWAYS = {
        'braintree': braintree.BraintreeGateway(BRAINTREE_CONFIG)
    }

    def __init__(self, name: str):
        self._get(name)

    def _get(self, name: str):
        self.processor = self.PAYMENT_GATEWAYS.get(name)

        if self.processor is None:
            raise InvalidPaymentProcessorPaymentInformation

    def create_customer(self, details: dict):
        result = self.processor.customer.create(details)

        if result.is_success is False:
            raise InvalidPaymentProcessorCustomerInformation

        return {
            'customer_id': result.customer.id
        }

    def create_payment_method(self, details: dict):
        payment_information = {}
        result = self.processor.credit_card.create(details)

        if result.is_success is False:
            raise InvalidPaymentProcessorPaymentInformation

        payment_information['payment_token'] = result.credit_card.token

        result = self.processor.payment_method_nonce.create(payment_information['payment_token'])

        if result.is_success is False:
            raise InvalidPaymentProcessorPaymentInformation

        payment_information['nonce_token'] = result.payment_method_nonce.nonce

        return payment_information
