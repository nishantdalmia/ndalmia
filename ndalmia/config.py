"""ndalmia.com development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SK = b'\xbe\x0c?\xf6\xb9 /\x1f\xc138\x94\x08\x18f\x05#N\x80\xb0\x0c\xec\xfcK'
SECRET_KEY = SK
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
NDALMIA_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = NDALMIA_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/ndalmia.sqlite3
DATABASE_FILENAME = NDALMIA_ROOT/'var'/'ndalmia.sqlite3'
