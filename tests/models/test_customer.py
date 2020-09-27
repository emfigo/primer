import pytest
import uuid

from primer import db
from primer.models.customer import Customer

@pytest.mark.usefixtures('database')
class TestCustomer:
    def test_creates_customer_with_all_expected_attributes(self, database):
        first_name = 'Test'
        last_name = 'Test1'
        company = 'Really Cool LTD'
        email = 'test1.lasttest@reallycool.test'
        phone = '+1111111111'
        fax = '+12222222222'
        website = 'https://www.reallycool.test'

        customer = Customer.create_customer(
            first_name=first_name,
            last_name=last_name,
            company=company,
            email=email,
            phone=phone,
            fax=fax,
            website=website
        )

        assert Customer.query.filter_by(
            email = email
        ).first().id == customer.id

        assert customer.id is not None

        assert Customer.query.filter_by(
            email = email
        ).first().token == customer.token
        assert customer.token is not None

        assert Customer.query.filter_by(
            email = email
        ).first().created_at == customer.created_at
        assert customer.created_at is not None

        assert Customer.query.filter_by(
            email = email
        ).first().updated_at == customer.updated_at
        assert customer.updated_at is not None

        assert customer.first_name == first_name
        assert customer.last_name == last_name
        assert customer.company == company
        assert customer.email == email
        assert customer.phone == phone
        assert customer.fax == fax
        assert customer.website == website

    def test_finds_by_email_returns_the_expected_customer(self, database):
        first_name = 'Test'
        last_name = 'Test2'
        company = 'Really Cool LTD'
        email = 'test2.lasttest@reallycool.test'
        phone = '+1111111111'
        fax = '+12222222222'
        website = 'https://www.reallycool.test'

        customer = Customer.create_customer(
            first_name=first_name,
            last_name=last_name,
            company=company,
            email=email,
            phone=phone,
            fax=fax,
            website=website
        )

        assert Customer.query.count() > 0
        assert Customer.find_by_email('nonexistingemail@something.test') is None
        assert Customer.find_by_email(email) == customer

    def test_finds_by_id_returns_the_expected_customer(self, database):
        first_name = 'Test'
        last_name = 'Test3'
        company = 'Really Cool LTD'
        email = 'test3.lasttest@reallycool.test'
        phone = '+1111111111'
        fax = '+12222222222'
        website = 'https://www.reallycool.test'

        customer = Customer.create_customer(
            first_name=first_name,
            last_name=last_name,
            company=company,
            email=email,
            phone=phone,
            fax=fax,
            website=website
        )

        assert Customer.query.count() > 0
        assert Customer.find_by_id(uuid.uuid4()) is None
        assert Customer.find_by_id(customer.id) == customer

    def test_finds_by_token_returns_the_expected_customer(self, database):
        first_name = 'Test'
        last_name = 'Test4'
        company = 'Really Cool LTD'
        email = 'test4.lasttest@reallycool.test'
        phone = '+1111111111'
        fax = '+12222222222'
        website = 'https://www.reallycool.test'

        customer = Customer.create_customer(
            first_name=first_name,
            last_name=last_name,
            company=company,
            email=email,
            phone=phone,
            fax=fax,
            website=website
        )

        assert Customer.query.count() > 0
        assert Customer.find_by_token('somenonexistingtoken') is None
        assert Customer.find_by_token(customer.token) == customer
