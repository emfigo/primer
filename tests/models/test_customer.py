import pytest

from primer import db
from primer.models.customer import Customer

@pytest.mark.usefixtures('database')
class TestCustomer:
    def test_creates_customer_with_all_expected_attributes(self, database):
        first_name = 'Test'
        last_name = 'LastTest'
        company = 'Really Cool LTD'
        email = 'test.lasttest@reallycool.test'
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

