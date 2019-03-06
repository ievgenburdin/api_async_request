import os
import string

API_HOST = os.environ['API_HOST']
API_URL = os.environ['API_URL']

DB_NAME = os.environ['DB_NAME']

DEBUG = True

ALPHABET_LIST = list(string.ascii_lowercase)

MAX_QUERY_LENGTH = 3
