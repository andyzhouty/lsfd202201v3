import os
SECRET_KEY = str(hash(os.getenv('SECRET_KEY')))
PASSWORD = hash(os.getenv('PASSWORD'))
ADMIN_PASSWORD = hash(os.getenv('ADMIN_PASSWORD'))
BOOTSTRAP_SERVE_LOCAL = True
