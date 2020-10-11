import braintree
from dotenv import load_dotenv, find_dotenv
import os
from os.path import join, dirname, exists

APP_ENV = os.environ.get('APP_ENV', 'dev')
DOTENV_PATH = join(dirname(__file__), f'.{APP_ENV}.env')

if exists(DOTENV_PATH):
    load_dotenv(dotenv_path=DOTENV_PATH)
else:
    load_dotenv(find_dotenv())


DATABASE_URI = os.environ['DATABASE_URI']

BRAINTREE_CONFIG = braintree.Configuration(
    braintree.Environment.Sandbox,
    merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
    public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
    private_key=os.environ.get('BRAINTREE_PRIVATE_KEY')
)
