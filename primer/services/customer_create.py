from primer.exceptions import InvalidCustomer
from primer.models.customer import Customer
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

    @classmethod
    def _slice(kls, details: dict) -> dict:
        sliced_details = {}

        for k in kls.MANDATORY_FIELDS:
            if details.get(k) is not None:
                sliced_details[k] = details[k]
            else:
                raise InvalidCustomer

        for k in kls.OPTIONAL_FIELDS:
            sliced_details[k] = details.get(k)


        return sliced_details

    @staticmethod
    def _register_customer_with_processor(processor_name: str, details: dict):
        processor = PaymentProcessors(processor_name)

        return processor.create_customer(details)

    @classmethod
    def call(kls, token: str, processor_name: str, details: dict):
        customer = Customer.find_by_token(token)

        if customer is None:
            sliced_details = kls._slice(details)
            customer = Customer.find_by_email(details['email'])

        if customer is None:
            processor_information = kls._register_customer_with_processor(processor_name, sliced_details)
            customer = Customer.create(**sliced_details)

            PaymentProcessorCustomerInformationCreate.call(
                processor_name,
                customer,
                processor_information
            )

        return customer

