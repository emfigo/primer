from http import HTTPStatus
import pytest

from primer.models.customer import Customer

@pytest.mark.usefixtures('testapp', 'database')
class TestBlueprintCustomers:
    def test_creates_customers_when_all_details_are_valid(self, testapp, database):
        client = testapp.test_client()
        email = 'test.test@reallycool.test'
        params = {
            'first_name': 'Test',
            'last_name': 'Test',
            'company': 'Really Cool LTD',
            'email': email,
            'phone': '+1111111111'
        }
        response = client.post('/customers', json=params)
        customer = Customer.find_by_email(email)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json == customer.as_dict()

    @pytest.mark.parametrize('invalid_detail', [
        { 'first_name': None },
        { 'last_name': None },
        { 'company': None },
        { 'email': None },
        { 'phone': None }
    ])
    def test_returns_an_error_when_missing_mandatory_field(self, testapp, database, invalid_detail):
        client = testapp.test_client()
        email = 'test.test@reallycool.test'
        params = {
            'first_name': 'Test',
            'last_name': 'Test',
            'company': 'Really Cool LTD',
            'email': email,
            'phone': '+1111111111'
        }
        response = client.post('/customers', json = {**params, **invalid_detail} )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == 'Customer details are invalid. Check; first_name, last_name, email, company, phone'
