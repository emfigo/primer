import pytest

from primer.exceptions import InvalidCustomer
from primer.services.customer_create import CustomerCreate
from primer.models.customer import Customer

@pytest.mark.usefixtures('database')
class TestCustomerCreate:
    first_name = 'Interesting'
    last_name = 'Test'
    company = 'Really Interesting LTD'
    email = 'interesting.test1@reallyinteresting.test'
    phone = '+1111111111'
    fax = '+12222222222'
    website = 'https://www.reallyinteresting.test'
    token = None

    details = {
        'first_name': first_name,
        'last_name': last_name,
        'company': company,
        'email': email,
        'phone': phone,
        'fax': fax,
        'website': website
    }

    processor_name = 'someprocessor'

    processor_information = {
        'some_field': 'some_info'
    }


    def test_when_customer_does_not_exists_and_all_details_correct_creates_customer(self, database, payment_processors):
        assert Customer.find_by_email(self.email) is None

        customer = CustomerCreate.call(self.token, self.processor_name, self.details)

        assert customer is not None
        assert Customer.find_by_email(self.email) == customer

    def test_when_customer_does_not_exists_and_with_extra_details_creates_customer(self, database, payment_processors):
        assert Customer.find_by_email(self.email) is None

        customer = CustomerCreate.call(self.token, self.processor_name, {**self.details, 'extra-attr': 'something' })

        assert customer is not None
        assert Customer.find_by_email(self.email) == customer

    def test_when_customer_exists_and_no_token_provided_returns_existing_customer(self, database, payment_processors):
        existing_customer = Customer.create(**self.details)

        customer = CustomerCreate.call(self.token, self.processor_name, self.details)

        assert existing_customer is not None
        assert existing_customer.id == customer.id

    def test_when_customer_exists_and_token_provided_returns_existing_customer(self, database, payment_processors):
        existing_customer = Customer.create(**self.details)

        customer = CustomerCreate.call(existing_customer.token, self.processor_name, self.details)

        assert existing_customer is not None
        assert existing_customer.id == customer.id
        assert existing_customer.token == customer.token

    @pytest.mark.parametrize('invalid_detail', [
        { 'first_name': None },
        { 'last_name': None },
        { 'company': None },
        { 'email': None },
        { 'phone': None }
    ])
    def test_when_customer_details_are_invalid_does_not_create_customer(self, database, invalid_detail, payment_processors):
        customer_counter = Customer.query.count()

        with pytest.raises(InvalidCustomer):
            customer = CustomerCreate.call(self.token, self.processor_name, {**self.details, **invalid_detail} )

        assert Customer.query.count() == customer_counter


    @pytest.mark.parametrize('optional_details', [
        { 'fax': None },
        { 'website': None }
    ])
    def test_when_customer_details_are_valid_and_optional_present_creates_customer(self, database, optional_details, payment_processors):
        customer_counter = Customer.query.count()

        customer = CustomerCreate.call(self.token, self.processor_name, {**self.details, **optional_details} )

        assert Customer.query.count() == customer_counter + 1
        assert customer is not None
        assert Customer.find_by_email(self.email) == customer
