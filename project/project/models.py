from project import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt
from project import app

ROLE_USER = 0
ROLE_OAUTH_USER = 1
ROLE_ADMIN = 2


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), index=True, unique=True, nullable=True)
    nickname = db.Column(db.String(40), index = True, unique = True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(60), index = True, unique=False, nullable=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    posts = db.relationship("Post", backref="author", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id, "exp": time() + expires_in},
                          app.config["SECRET_KEY"], algorithm="HS256").decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"],
                            algorithms=["HS256"])["reset_password"]
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return "<User %r>" % self.nickname


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)