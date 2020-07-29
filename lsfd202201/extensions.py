from flask_bootstrap import Bootstrap
from flask_share import Share
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_mail import Mail

bootstrap = Bootstrap()
share = Share()
db = SQLAlchemy()
csrf = CSRFProtect()
ckeditor = CKEditor()
migrate = Migrate()
mail = Mail()
