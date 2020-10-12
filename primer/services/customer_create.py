from primer.models.customer import Customer
from primer.services import utils
from primer.services.payment_processor_customer_information_create import PaymentProcessorCustomerInformationCreate
from primer.payment_processors import PaymentProcessors

class CustomerCreate:
    MANDATORY_FIELDS = [
        'first_name',
        'last_name',
        'company',
        'email',
        'phone'
    ]

    OPTIONAL_FIELDS = [
        'fax',
        'website'
    ]

    def __init__(self, customer_token: str, processor_name: str, details: dict):
        self.customer_token = customer_token
        self.processor_name = processor_name
        self.details = utils.slice(CustomerCreate, details)

    def _register_customer_with_processor(self, processor_name: str, details: dict):
        processor = PaymentProcessors(processor_name)

        return processor.create_customer(details)

    def create_customer(self):
        customer = Customer.find_by_token(self.customer_token)

        if customer is None:
            customer = Customer.find_by_email(self.details['email'])

        if customer is None:
            processor_information = self._register_customer_with_processor(
                self.processor_name, self.details
            )

            customer = Customer.create(**self.details)

            PaymentProcessorCustomerInformationCreate.call(
                self.processor_name,
                customer,
                processor_information
            )

        return customer

    @classmethod
    def call(kls, customer_token: str, processor_name: str, details: dict):
        service = kls(customer_token, processor_name, details)

        return service.create_customer()

