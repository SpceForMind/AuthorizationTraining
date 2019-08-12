import os
from project.local_settings import _MAIL_PASSWORD, _SECRET_KEY
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # активирует предотвращение поддельных межсайтовых запросов
    CSRF_ENABLED = True

    # when enabled CSRF this option generate crypto-token for validating forms
    SECRET_KEY = _SECRET_KEY

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dummy.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = "spaceformind19@gmail.com"
    MAIL_PASSWORD = _MAIL_PASSWORD
    ADMINS = ['spaceformind19@gmail.com']

    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '2365857986826968',
            'secret': 'ffbb70776d613f668e395a2affd94ef7'
        },
        "github": {
            "id": "e863cc5cca6fb1366dda",
            "secret": "43b4b37e870f3dad2e9d45e7283d96a998188923"
        }
    }

    SERVER_NAME = os.environ.get("SERVER_NAME") or "localhost:5000"
