from http import HTTPStatus
import pytest

from primer.models.customer import Customer

@pytest.mark.usefixtures('testapp', 'database', 'payment_processors')
class TestBlueprintCustomers:
    params = {
        'first_name': 'Test',
        'last_name': 'Test',
        'company': 'Really Cool LTD',
        'email': 'test.test@reallycool.test',
        'phone': '+1111111111'
    }


    def test_creates_customers_when_all_details_are_valid(self, testapp, database, payment_processors):
        client = testapp.test_client()
        response = client.post('/customers', json=self.params)
        customer = Customer.find_by_email(self.params['email'])

        assert response.status_code == HTTPStatus.CREATED
        assert response.json == customer.as_dict()

    def test_returns_existing_customers_when_token_specified(self, testapp, database, payment_processors):
        client = testapp.test_client()
        email = 'test.test@reallycool.test'
        customer = Customer.create(**self.params)
        headers = {
            'Authorization': f'Bearer {customer.token}'
        }
        response = client.post('/customers', json=self.params, headers=headers)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json == customer.as_dict()

    @pytest.mark.parametrize('invalid_detail', [
        { 'first_name': None },
        { 'last_name': None },
        { 'company': None },
        { 'email': None },
        { 'phone': None }
    ])
    def test_returns_an_error_when_missing_mandatory_field(self, testapp, database, invalid_detail, payment_processors):
        client = testapp.test_client()
        response = client.post('/customers', json = {**self.params, **invalid_detail} )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == 'Customer details are invalid. Check; first_name, last_name, email, company, phone'
