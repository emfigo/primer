import pytest
import uuid

from primer.models.customer import Customer

@pytest.mark.usefixtures('database')
class TestCustomer:
    first_name = 'Test'
    last_name = 'Test'
    company = 'Really Cool LTD'
    email = 'test.test@reallycool.test'
    phone = '+1111111111'
    fax = '+12222222222'
    website = 'https://www.reallycool.test'

    def test_creates_customer_with_all_expected_attributes(self, database):
        customer = Customer.create(
            first_name = self.first_name,
            last_name = self.last_name,
            company = self.company,
            email = self.email,
            phone = self.phone,
            fax = self.fax,
            website = self.website
        )

        assert Customer.query.filter_by(
            email = self.email
        ).first().id == customer.id

        assert customer.id is not None

        assert Customer.query.filter_by(
            email = self.email
        ).first().token == customer.token
        assert customer.token is not None

        assert Customer.query.filter_by(
            email = self.email
        ).first().created_at == customer.created_at
        assert customer.created_at is not None

        assert Customer.query.filter_by(
            email = self.email
        ).first().updated_at == customer.updated_at
        assert customer.updated_at is not None

        assert customer.first_name == self.first_name
        assert customer.last_name == self.last_name
        assert customer.company == self.company
        assert customer.email == self.email
        assert customer.phone == self.phone
        assert customer.fax == self.fax
        assert customer.website == self.website

    def test_converts_customer_to_dict(self, database):
        customer = Customer.create(
            first_name = self.first_name,
            last_name = self.last_name,
            company = self.company,
            email = self.email,
            phone = self.phone,
            fax = self.fax,
            website = self.website
        )

        expected_json = {
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'token': customer.token,
            'updated_at': int(customer.created_at.timestamp()),
            'created_at': int(customer.created_at.timestamp())
        }

        assert customer.as_dict() == expected_json

    def test_finds_by_email_returns_the_expected_customer(self, database):
        customer = Customer.create(
            first_name = self.first_name,
            last_name = self.last_name,
            company = self.company,
            email = self.email,
            phone = self.phone,
            fax = self.fax,
            website = self.website
        )

        assert Customer.query.count() == 1
        assert Customer.find_by_email('nonexistingemail@something.test') is None
        assert Customer.find_by_email(self.email) == customer

    def test_finds_by_id_returns_the_expected_customer(self, database):
        customer = Customer.create(
            first_name = self.first_name,
            last_name = self.last_name,
            company = self.company,
            email = self.email,
            phone = self.phone,
            fax = self.fax,
            website = self.website
        )

        assert Customer.query.count() == 1
        assert Customer.find_by_id(uuid.uuid4()) is None
        assert Customer.find_by_id(customer.id) == customer

    def test_finds_by_token_returns_the_expected_customer(self, database):
        customer = Customer.create(
            first_name = self.first_name,
            last_name = self.last_name,
            company = self.company,
            email = self.email,
            phone = self.phone,
            fax = self.fax,
            website = self.website
        )

        assert Customer.query.count() == 1
        assert Customer.find_by_token('somenonexistingtoken') is None
        assert Customer.find_by_token(customer.token) == customer
