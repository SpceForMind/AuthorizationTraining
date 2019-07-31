from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from project import app, db, lm
from project.forms import LoginForm
from project.models import User, ROLE_USER, ROLE_ADMIN

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

    if registred_user is None:
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

    user = User(nickname=request.form["username"], email=request.form["email"], password=request.form["password"], role=ROLE_USER)
    db.session.add(user)
    db.session.commit()
    flash("User successfully registrated")

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


