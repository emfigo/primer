import braintree

from config import BRAINTREE_CONFIG
from primer.exceptions import InvalidPaymentProcessorPaymentInformation, InvalidPaymentMethod, InvalidPaymentProcessorCustomerInformation

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
        result = self.processor.credit_card.create(details)

        if result.is_success is False:
            raise InvalidPaymentProcessorPaymentInformation

        return {
            'payment_token': result.credit_card.token
        }

    def create_payment_method_nonce(self, details):
        result = self.processor.payment_method_nonce.create(details['payment_token'])

        if result.is_success is False:
            raise InvalidPaymentProcessorPaymentInformation

        return {
            'payment_method_nonce': result.payment_method_nonce.nonce
        }


    def create_sale(self, details: dict):
        result = self.processor.transaction.sale(details)

        if result.is_success is False:
            raise InvalidPaymentMethod

        return result.is_success
