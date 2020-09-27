import hashlib

from primer.tokenizer import Tokenizer

class TestTokenizer:
    def test_from_simple_info_returns_expected_token_if_applies_correct_algorithm(self):
        # All the numbers in the info are the same so the tokenizer algorithm won't
        # introduce much entropy. In reality this won't happen for payment information or how
        # we are going to construct this info string, so this is used for testing only.
        info = '1111' * 4
        knowned_transformation = '1' * Tokenizer.TOKEN_SIZE

        expected_output = str(hashlib.sha256(knowned_transformation.encode()).hexdigest())

        assert Tokenizer.token_from(info) == expected_output

    def test_from_complex_info_cannot_predict_token_if_applies_only_hashing(self):
        # To the previous test if we just add the expiry date of a card, plus the
        # cvv, there is no way we can predict the token, even though we are using
        # the same numbers. (This is alse based on what we have used in the class).
        info = ('1111' * 4) + '11/11' + '111'
        knowned_transformation = '1' * Tokenizer.TOKEN_SIZE

        hashed_output = str(hashlib.sha256(knowned_transformation.encode()).hexdigest())

        assert Tokenizer.token_from(info) is not None
        assert Tokenizer.token_from(info) != hashed_output

    def test_random_token_is_generated_correctly(self):
        assert Tokenizer.random_token() is not None
        assert type(Tokenizer.random_token()) is str
        assert len(Tokenizer.random_token()) == 64
