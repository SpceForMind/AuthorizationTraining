# AuthorizationTraining

### Authorization types:
+ Base sing up/ sing in
+ OAuth2.0 via Github/Facebook

### Security and Data recovery
+ Werkzeug(hash generating)
+ JWT token creator
+ Email confirmation(Registration/Forgot password)

### Run
In the directory **project** execute **run.sh**:
````
./run.sh
````

### Database migration(SQLite)
In the directory **project/project** execute **manage.py**:
````
python3 manage.py db [COMMAND]
# [COMMANDS]:
# migrate - to commit models.py changes
# upgrade - to upgrade database tables
````

### View database content:
In the directory **project** **execute debug.sh**:
````
./debug.sh
# db - database object(sqlalchemy)
# User - user model
# Post - post model
````

### Tools
+ Flask
+ SQLAlchemy(SQLite flask-wrapper)
+ rauth(OAuth2.0 implementation)