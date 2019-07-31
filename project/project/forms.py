from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, validators


class LoginForm(FlaskForm):
    # available authorization through provider OpenID
    openid = StringField('openid', validators = [validators.Required()])

    # check box for creating cookies
    remember_me = BooleanField('remember_me', default = False)