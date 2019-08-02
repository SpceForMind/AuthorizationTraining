#!/usr/bin/env bash

# setup path to the flask shell application
export FLASK_APP=project.auth_training.py

# setup mode
export FLASK_ENV=development

# install project in virtual enviroment(searching for setup.py)
pip3 install -e .

# activate flask shell
flask shell