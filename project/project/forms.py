from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, validators


class LoginForm(FlaskForm):
    # available authorization through provider OpenID
    openid = StringField('openid')

    # check box for creating cookies
    remember_me = BooleanField('remember_me', default = False)


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[validators.DataRequired(),
                                                     validators.Length(min=8, max=30)])
    password2 = PasswordField("Repeat Password",
                              validators=[validators.DataRequired(),
                                          validators.Length(min=8, max=30),
                                          validators.EqualTo("password")])
    submit = SubmitField("Request Password Reset")