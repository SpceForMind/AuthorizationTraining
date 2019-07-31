from project import db, app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)

# creating manage.py
manager = Manager(app)
manager.add_command("db", MigrateCommand)

# include table models
from project import models

if __name__ == "__main__":
    manager.run()