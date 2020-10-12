import pytest

from primer.services.customer_create import CustomerCreate
from primer.exceptions import InvalidCustomer, InvalidPaymentMethod, InvalidSale
from primer.services.payment_method_create import PaymentMethodCreate
from primer.services.sale_create import SaleCreate

@pytest.mark.usefixtures('database', 'payment_processors')
class TestSaleCreate:
    customer_details = {
        'first_name': 'Interesting',
        'last_name': 'Test',
        'company': 'Really Interesting LTD',
        'email': 'interesting.test1@reallyinteresting.test',
        'phone': '+1111111111',
        'fax': '+12222222222',
        'website': 'https://www.reallyinteresting.test'
    }

    payment_details = {
        'cardholder_name': 'Test Coool',
        'number': '1111' * 4,
        'cvv': '111',
        'expiration_date': '12/99'
    }

    sale_details = {
        'amount': '100.00'
    }

    processor_name = 'someprocessor'

    def test_creates_sale_when_all_details_are_valid_and_valid_tokens_provided(self, database, payment_processors):
        customer = CustomerCreate.call(
            None,
            self.processor_name,
            self.customer_details
        )
        payment_method = PaymentMethodCreate.call(
            self.processor_name,
            customer.token,
            None,
            self.payment_details
        )

        sale = SaleCreate.call(
            self.processor_name,
            customer.token,
            payment_method.token,
            self.sale_details
        )

        assert sale == { 'message': f"transaction was made successfully for amount {self.sale_details['amount']}" }

    def test_when_payment_details_are_valid_and_no_payment_token_provided_does_not_create_sale(self, database, payment_processors):

        customer = CustomerCreate.call(
            None,
            self.processor_name,
            self.customer_details
        )

        with pytest.raises(InvalidPaymentMethod):
            SaleCreate.call(
                self.processor_name,
                customer.token,
                None,
                self.sale_details
            )

    def test_when_payment_details_are_valid_and_no_customer_token_provided_does_not_create_sale(self, database, payment_processors):

        customer = CustomerCreate.call(
            None,
            self.processor_name,
            self.customer_details
        )
        payment_method = PaymentMethodCreate.call(
            self.processor_name,
            customer.token,
            None,
            self.payment_details
        )

        with pytest.raises(InvalidCustomer):
            SaleCreate.call(
                self.processor_name,
                None,
                payment_method.token,
                self.sale_details
            )

    @pytest.mark.parametrize('invalid_detail', [
        { 'amount': None }
    ])
    def test_when_payment_details_are_invalid_does_not_create_sale(self, database, invalid_detail, payment_processors):

        customer = CustomerCreate.call(
            None,
            self.processor_name,
            self.customer_details
        )
        payment_method = PaymentMethodCreate.call(
            self.processor_name,
            customer.token,
            None,
            self.payment_details
        )

        with pytest.raises(InvalidSale):
            SaleCreate.call(
                self.processor_name,
                customer.token,
                payment_method.token,
                {**self.sale_details, **invalid_detail}
            )


