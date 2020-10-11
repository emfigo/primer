from http import HTTPStatus
import pytest

from primer.models.customer import Customer
from primer.models.payment_processor_customer_information import PaymentProcessorCustomerInformation
from primer.models.payment_method import PaymentMethod

@pytest.mark.usefixtures('testapp', 'database', 'payment_processors')
class TestBlueprintPaymentMethods:
    def test_creates_payment_method_when_all_details_are_valid(self, testapp, database, payment_processors):
        client = testapp.test_client()
        customer = Customer.create(**{
            'first_name': 'Test',
            'last_name': 'Test',
            'company': 'Really Cool LTD',
            'email': 'test.test@reallycool.test',
            'phone': '+1111111111'
        })

        customer_information = {
            'customer_id': 'someid'
        }

        payment_processor_customer_information =  PaymentProcessorCustomerInformation.create(
            name = 'braintree',
            customer = customer,
            information = customer_information
        )

        params = {
            'cardholder_name': 'Test Coool',
            'number': '4005519200000004',
            'cvv': '111',
            'expiration_date': '12/99'
        }

        headers = {
            'Authorization': f'Bearer {customer.token}',
        }
        response = client.post('/payment_methods', json=params, headers=headers)

        assert response.status_code == HTTPStatus.CREATED
        assert PaymentMethod.find_by_token(response.json['token']) is not None

    def test_returns_existing_payment_method_when_token_specified(self, testapp, database, payment_processors):
        client = testapp.test_client()
        customer = Customer.create(**{
            'first_name': 'Test',
            'last_name': 'Test',
            'company': 'Really Cool LTD',
            'email': 'test.test@reallycool.test',
            'phone': '+1111111111'
        })
        customer_information = {
            'customer_id': 'someid'
        }

        payment_processor_customer_information =  PaymentProcessorCustomerInformation.create(
            name = 'braintree',
            customer = customer,
            information = customer_information
        )

        params = {
            'cardholder_name': 'Test Coool',
            'number': '4005519200000004',
            'cvv': '111',
            'expiration_date': '12/99'
        }
        payment_method = PaymentMethod.create(
            customer = customer,
            details = params,
        )
        headers = {
            'Authorization': f'Bearer {customer.token}',
            'X-pay-token': f'{payment_method.token}'
        }
        response = client.post('/payment_methods', json=params, headers=headers)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json['token'] == payment_method.token

    @pytest.mark.parametrize('invalid_detail', [
        { 'cardholder_name': None },
        { 'number': None },
        { 'cvv': None },
        { 'expiration_date': None }
    ])
    def test_returns_an_error_when_missing_mandatory_field(self, testapp, database, invalid_detail, payment_processors):
        client = testapp.test_client()
        customer = Customer.create(**{
            'first_name': 'Test',
            'last_name': 'Test',
            'company': 'Really Cool LTD',
            'email': 'test.test@reallycool.test',
            'phone': '+1111111111'
        })
        customer_information = {
            'customer_id': 'someid'
        }

        payment_processor_customer_information =  PaymentProcessorCustomerInformation.create(
            name = 'braintree',
            customer = customer,
            information = customer_information
        )
        params = {
            'cardholder_name': 'Test Coool',
            'number': '4005519200000004',
            'cvv': '111',
            'expiration_date': '12/99'
        }
        headers = {
            'Authorization': f'Bearer {customer.token}',
        }
        response = client.post('/payment_methods', json={**params, **invalid_detail}, headers=headers)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json == 'The payment method details are invalid. Please try new details'

