# активирует предотвращение поддельных межсайтовых запросов
CSRF_ENABLED = True

# when enabled CSRF this option generate crypto-token for validating forms
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': "VK", "url": "http://vkontakteid.ru/"},
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

# setting data base
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'simple.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')