import os

SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key"
DEBUG = True

MAX_CONTENT_LENGTH = 3 * 1024 * 1024