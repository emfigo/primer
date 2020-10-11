from flask import Blueprint, request, jsonify
from http import HTTPStatus

from primer.blueprints.utils import get_token, get_payment_token
from primer.exceptions import InvalidPaymentMethod, InvalidPaymentProcessorPaymentInformation
from primer.services.payment_method_create import PaymentMethodCreate

payment_methods = Blueprint('payment_methods', __name__)

PAYMENT_PROCESSOR = 'braintree'

@payment_methods.route('/payment_methods', methods=['POST'])
def create():
    customer_token = get_token(request.headers)
    payment_token = get_payment_token(request.headers)
    try:
        payment_method = PaymentMethodCreate.call(PAYMENT_PROCESSOR, customer_token, payment_token, request.json)
    except (InvalidPaymentMethod, InvalidPaymentProcessorPaymentInformation):
        return jsonify('The payment method details are invalid. Please try new details'), HTTPStatus.BAD_REQUEST

    return jsonify(payment_method.as_dict()), HTTPStatus.CREATED
