#!/usr/bin/env bash

# setup path to the application
export FLASK_APP=project

# setup mode
export FLASK_ENV=development

export SERVER_NAME=localhost:5000

# install project in virtual enviroment(searching for setup.py)
pip3 install -e .

# run the application
flask run