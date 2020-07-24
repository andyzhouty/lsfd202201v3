import os
from werkzeug.security import generate_password_hash

class Base:
    SECRET_KEY = generate_password_hash(os.getenv('SECRET_KEY'))
    PASSWORD = generate_password_hash(os.getenv('PASSWORD'))
    ADMIN_PASSWORD = generate_password_hash(os.getenv('ADMIN_PASSWORD'))
    BOOTSTRAP_SERVE_LOCAL = True

class Production(Base):
    DEBUG=False

class Development(Base):
    DEBUG=True

config = {
    'production': Production,
    'development': Development
}
