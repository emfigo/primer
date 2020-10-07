from datetime import datetime
from dateutil import parser
from flask import Blueprint, request, jsonify
from http import HTTPStatus

from primer.exceptions import InvalidCustomer
from primer.services.customer_create import CustomerCreate

customers = Blueprint('customers', __name__)

@customers.route('/customers', methods=['POST'])
def create():
    token = None
    try:
        customer = CustomerCreate.call(token, request.json)
    except InvalidCustomer:
        return jsonify('Customer details are invalid. Check; first_name, last_name, email, company, phone'), HTTPStatus.BAD_REQUEST

    return jsonify(customer.as_dict()), HTTPStatus.CREATED
