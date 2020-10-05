import pytest
import uuid

from primer.exceptions import InvalidCustomer
from primer.services.customer_create import CustomerCreate
from primer.models.customer import Customer

@pytest.mark.usefixtures('database')
class TestCustomerCreate:
    def test_when_customer_does_not_exists_and_all_details_correct_creates_customer(self, database):
        first_name = 'Interesting'
        last_name = 'Test1'
        company = 'Really Interesting LTD'
        email = 'interesting.test1@reallyinteresting.test'
        phone = '+1111111111'
        fax = '+12222222222'
        website = 'https://www.reallyinteresting.test'

        details = {
            'first_name': first_name,
            'last_name': last_name,
            'company': company,
            'email': email,
            'phone': phone,
            'fax': fax,
            'website': website
        }

        assert Customer.find_by_email(email) is None

        customer = CustomerCreate.call(details)

        assert customer is not None
        assert Customer.find_by_email(email) == customer

    def test_when_customer_exists_returns_existing_customer(self, database):
        first_name = 'Interesting'
        last_name = 'Test2'
        company = 'Really Interesting LTD'
        email = 'interesting.test2@reallyinteresting.test'
        phone = '+1111111111'
        fax = '+12222222222'
        website = 'https://www.reallyinteresting.test'

        details = {
            'first_name': first_name,
            'last_name': last_name,
            'company': company,
            'email': email,
            'phone': phone,
            'fax': fax,
            'website': website
        }

        existing_customer = Customer.create(**details)

        customer = CustomerCreate.call(details)

        assert existing_customer is not None
        assert existing_customer.id == customer.id

    @pytest.mark.parametrize('invalid_detail', [
        { 'first_name': None },
        { 'last_name': None },
        { 'company': None },
        { 'email': None },
        { 'phone': None }
    ])
    def test_when_customer_details_are_invalid_does_not_create_customer(self, database, invalid_detail):
        first_name = 'Interesting'
        last_name = 'Test3'
        company = 'Really Interesting LTD'
        email = 'interesting.test3@reallyinteresting.test'
        phone = '+1111111111'
        fax = '+12222222222'
        website = 'https://www.reallyinteresting.test'

        details = {
            'first_name': first_name,
            'last_name': last_name,
            'company': company,
            'email': email,
            'phone': phone,
            'fax': fax,
            'website': website
        }

        customer_counter = Customer.query.count()

        with pytest.raises(InvalidCustomer):
            customer = CustomerCreate.call( {**details, **invalid_detail} )

        assert Customer.query.count() == customer_counter


    @pytest.mark.parametrize('optional_details', [
        { 'fax': None },
        { 'website': None }
    ])
    def test_when_customer_details_are_valid_and_optional_present_creates_customer(self, database, optional_details):
        first_name = 'Interesting'
        last_name = 'Test'
        company = 'Really Interesting LTD'
        email = 'interesting.test@reallyinteresting.test'
        phone = '+1111111111'
        fax = '+12222222222'
        website = 'https://www.reallyinteresting.test'

        details = {
            'first_name': first_name,
            'last_name': last_name,
            'company': company,
            'email': email,
            'phone': phone,
            'fax': fax,
            'website': website
        }

        customer_counter = Customer.query.count()

        customer = CustomerCreate.call( {**details, **optional_details} )

        assert Customer.query.count() == customer_counter + 1
        assert customer is not None
        assert Customer.find_by_email(email) == customer
