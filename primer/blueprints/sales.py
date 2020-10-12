
from flask import Blueprint, request, jsonify
from http import HTTPStatus

from primer.blueprints.utils import get_token, get_payment_token
from primer.exceptions import InvalidPaymentMethod, InvalidCustomer
from primer.services.sale_create import SaleCreate

sales = Blueprint('sales', __name__)

PAYMENT_PROCESSOR = 'braintree'

@sales.route('/sales', methods=['POST'])
def create():
    customer_token = get_token(request.headers)
    payment_token = get_payment_token(request.headers)
    try:
        sale = SaleCreate.call(PAYMENT_PROCESSOR, customer_token, payment_token, request.json)
    except (InvalidPaymentMethod, InvalidCustomer):
        return jsonify('The customer or/and the payment token or amount are invalid. Please try new tokens or amount.'), HTTPStatus.BAD_REQUEST

    return jsonify(sale), HTTPStatus.CREATED
