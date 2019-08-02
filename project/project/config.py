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
