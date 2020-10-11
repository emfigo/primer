def get_token(headers):
    token = None

    if headers.get('Authorization'):
        token = headers['Authorization'].split()[-1]

    return token

def get_payment_token(headers):
    token = None

    if headers.get('X-pay-token'):
        token = headers['X-pay-token']

    return token
