from primer.exceptions import InvalidCustomer
from primer.models.customer import Customer

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
    def call(kls, token: str, details: dict):
        customer = Customer.find_by_token(token)

        if customer is None:
            sliced_details = kls._slice(details)
            customer = Customer.find_by_email(details['email'])

        if customer is None:
            customer = Customer.create(**sliced_details)

        return customer

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


