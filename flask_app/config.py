import os
import random
import string

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', "".join(random.choices(string.ascii_uppercase + string.digits, k=20)))
