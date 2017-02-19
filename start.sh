#!/usr/bin/env bash

source ./venv/bin/activate

export FLASK_APP=core_app.py
flask run --host=0.0.0.0 --port=5002