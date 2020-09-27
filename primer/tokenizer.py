import hashlib
import secrets

class Tokenizer:
    """
    This class is heavily based on the core library used in python called secrets. This
    library already contains basics for what is required for constructing good tokenization.
    Anything more complex can be analysed individually based on requirements.
    For more information read:
    https://docs.python.org/3/library/secrets.html
    https://www.python.org/dev/peps/pep-0506/

    """

    # To represent an ascii character is necessary only 1 byte. As for now, it is believed
    # that 32 bytes (256 bits) of randomness is sufficient for the typical use-case expected.
    # Said that, if all the characters are too similar, will introduce a higher probability
    # of guessing, so 256 bytes makes it easier to introduce more entropy and makes it harder
    # to guess. Also this fits well with the hashing we are using.
    # For more information go to https://docs.python.org/3/library/secrets.html
    TOKEN_SIZE = 256

    @classmethod
    def random_token(kls) -> str:
        return str(hashlib.sha256(secrets.token_urlsafe(kls.TOKEN_SIZE).encode()).hexdigest())

    @classmethod
    def token_from(kls, info: str) -> str:
        password = ''.join(secrets.choice(info) for i in range(kls.TOKEN_SIZE))

        # For adding an extra layer of security and to not identify from where the token comes
        # from, once is generated from the info variable, this algorithm hashes the end result
        # using the hashing algorithm SHA256. There are several hashing algorithm that are better
        # than this one, but with the tokenization, enough entropy was introduced in the info
        # variable to require a more complex solution for now (unless the contrary is proved to
        # be needed).
        return str(hashlib.sha256(password.encode()).hexdigest())
