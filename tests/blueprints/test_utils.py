from primer.blueprints import utils

class TestBluePrintsUtils:
    def test_get_token_returns_none_when_no_token_present(self):
        headers = {}

        assert utils.get_token(headers) is None

    def test_get_token_returns_token_when_token_present(self):
        headers = {'Authorization': 'Bearer sometoken'}

        assert utils.get_token(headers) == 'sometoken'
