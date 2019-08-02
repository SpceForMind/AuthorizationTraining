from project import db, app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)

with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)

# creating manage.py
manager = Manager(app)
manager.add_command("db", MigrateCommand)

# include table models
from project import models

if __name__ == "__main__":
    manager.run()