from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from project import app, db, lm
from project.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from project.models import User, ROLE_USER, ROLE_ADMIN
from project.mail import send_password_reset_email, send_confirm_email
from project.oauth import OAuthSignIn

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template('index.html',
        title = 'Home',
        user = user,
        posts = posts)


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("login.html",
                               title = "Sign In")

    username = request.form["username"]
    password = request.form["password"]
    registred_user = User.query.filter_by(nickname=username).first()

    if registred_user is None or not registred_user.check_password(password):
        flash("Username or Password is invalid", "error")
        return redirect(url_for("login"))

    remember_me = False

    if remember_me in request.form:
        remember_me = True

    login_user(registred_user, remember=remember_me)
    flash("Logged in successfully")

    return redirect(request.args.get("next") or url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if User.query.filter_by(nickname=request.form["username"]).first() is not None:
        flash("User with username %s already registrated" % request.form["username"])
        return redirect(url_for("register"))

    if User.query.filter_by(email=request.form["email"]).first() is not None:
        flash("User with email %s already registrated" % request.form["email"])

    user = User(nickname=request.form["username"], email=request.form["email"], role=ROLE_USER)
    user.set_password(request.form["password"])
    send_confirm_email(user=user)
    flash("Check received email address for confirm registration")

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    '''Reset password request function

    :return GET - reset password form; POST - send mail at the received mail with crypto token
    put in the mail link:
    '''
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password")

        return redirect(url_for("login"))
    return render_template("reset_password_request.html",
                           title = "Reset Password", form = form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    '''Reset password function

    :param token - is a token whick was received by <reser_password_request> function:
    :return GET - reset password page; POST - redirect to login page:
    '''
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("index"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("login"))

    return render_template("reset_password.html",
                           title = "Reset Password",
                           form=form)


@app.route("/confirm_email_registration/<token>")
def confirm_email_registration(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    user = User.verify_confirm_email_token(token=token)
    if not user:
        return redirect(url_for("index"))

    db.session.add(user)
    db.session.commit()
    flash("Email has been confirmed successfully")

    return redirect(url_for("login"))

@app.route("/authorize/<provider>/")
def oauth_authorize(provider):
    '''Common function for user authorize through @provider

    :param provider is a Auth2.0 provider:
    :return call function whick make redirect to @provider authorize page:
    '''
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    oauth = OAuthSignIn.get_provider(provider)
    print("AUTORIZE", oauth)
    return oauth.authorize()


@app.route("/callback/<provider>/")
def oauth_callback(provider):
    '''Common function for @provider callback OAuth2.0 stage

    :param provider is a OAuth2.0 provider:
    :return redirect to home page:
    '''
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    oauth = OAuthSignIn.get_provider(provider)
    print(oauth)
    social_id, username = oauth.callback()
    if social_id is None:
        flash("Authentication failed.")
        return redirect(url_for("index"))

    user = User.query.filter_by(social_id=social_id).first()
    if user is None:
        user = User(social_id=social_id, nickname=username)
        db.session.add(user)
        db.session.commit()

    login_user(user, True)

    return redirect(url_for("index"))