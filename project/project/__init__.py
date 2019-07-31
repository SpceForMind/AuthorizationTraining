import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from project.config import basedir

# Initialization of application (1/3)
app = Flask(__name__)
app.config.from_object("project.config")

db = SQLAlchemy(app)

lm = LoginManager(app)
lm.login_view = "login"

#  Routing (2/3)
import project.views

# Run application (3/3)
if __name__ == "__main__":
    app.run(debug=True)