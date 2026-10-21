import os

SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"
DEBUG = True