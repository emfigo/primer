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

