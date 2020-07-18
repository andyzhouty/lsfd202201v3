import os
SECRET_KEY = str(hash(os.getenv('SECRET_KEY')))
PASSWORD = str(hash(os.getenv('PASSWORD')))
ADMIN_PASSWORD = str(hash(os.getenv('ADMIN_PASSWORD')))
BOOTSTRAP_SERVE_LOCAL = True
