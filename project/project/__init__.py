from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from project.config import Config

# Initialization of application (1/3)
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

lm = LoginManager(app)
lm.login_view = "login"

mail = Mail(app)

#  Routing (2/3)
import project.views

# Run application (3/3)
if __name__ == "__main__":
    app.run(debug=True, host="localhost")