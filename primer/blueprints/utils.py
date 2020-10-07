def get_token(headers):
    token = None

    if headers.get('Authorization'):
        token = headers['Authorization'].split()[-1]

    return token

