from http import HTTPStatus
import pytest

from primer.services.customer_create import CustomerCreate
from primer.services.payment_method_create import PaymentMethodCreate

@pytest.mark.usefixtures('testapp', 'database', 'payment_processors')
class TestBlueprintPaymentMethods:
    customer_details = {
        'first_name': 'test',
        'last_name': 'Test',
        'company': 'Really Cool LTD',
        'email': 'test.test@reallycool.test',
        'phone': '+1111111111'
    }

    payment_method_details = {
        'cardholder_name': 'Test Coool',
        'number': '4005519200000004',
        'cvv': '111',
        'expiration_date': '12/99'
    }

    details = {
        'amount': '100.00'
    }

    processor_name = 'braintree'

    def test_creates_sale_when_all_details_are_valid(self, testapp, database, payment_processors):
        client = testapp.test_client()
        customer = CustomerCreate.call(
            None,
            self.processor_name,
            self.customer_details
        )

        payment_method = PaymentMethodCreate.call(
            'braintree',
            customer.token,
            None,
            self.payment_method_details
        )

        headers = {
            'Authorization': f'Bearer {customer.token}',
            'X-pay-token': f'{payment_method.token}'
        }
        response = client.post('/sales', json=self.details, headers=headers)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json == { 'message': 'transaction was made successfully for amount 100.00' }

    @pytest.mark.parametrize('invalid_header', [
        'Authorization',
       'X-pay-token'
    ])
    def test_returns_an_error_when_missing_mandatory_token(self, testapp, database, invalid_header, payment_processors):
        client = testapp.test_client()
        customer = CustomerCreate.call(
            None,
            self.processor_name,
            self.customer_details
        )

        payment_method = PaymentMethodCreate.call(
            'braintree',
            customer.token,
            None,
            self.payment_method_details
        )

        headers = {
            'Authorization': f'Bearer {customer.token}',
            'X-pay-token': f'{payment_method.token}'
        }

        headers.pop(invalid_header)

        response = client.post('/sales', json=self.details, headers=headers)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == 'The customer or/and the payment token are invalid. Please try new tokens.'

    @pytest.mark.parametrize('invalid_detail', [
        { 'amount': None }
    ])
    def test_returns_an_error_when_missing_mandatory_field(self, testapp, database, invalid_detail, payment_processors):
        client = testapp.test_client()
        customer = CustomerCreate.call(
            None,
            'braintree',
            self.customer_details
        )

        payment_method = PaymentMethodCreate.call(
            self.processor_name,
            customer.token,
            None,
            self.payment_method_details
        )

        headers = {
            'Authorization': f'Bearer {customer.token}',
            'X-pay-token': f'{payment_method.token}'
        }

        response = client.post('/sales', json={**self.details, **invalid_detail}, headers=headers)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == 'The customer or/and the payment token are invalid. Please try new tokens.'
    @pytest.mark.parametrize('invalid_detail', [
        { 'amount': None }
    ])
    def test_returns_an_error_when_missing_mandatory_field(self, testapp, database, invalid_detail, payment_processors):
        client = testapp.test_client()
        customer = CustomerCreate.call(
            None,
            self.processor_name,
            self.customer_details
        )

        payment_method = PaymentMethodCreate.call(
            self.processor_name,
            customer.token,
            None,
            self.payment_method_details
        )

        headers = {
            'Authorization': f'Bearer {customer.token}',
            'X-pay-token': f'{payment_method.token}'
        }

        response = client.post('/sales', json={**self.details, **invalid_detail}, headers=headers)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == 'The camount is not provided. Please try new amount.'


