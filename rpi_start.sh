#!/usr/bin/env bash

source /home/sanya/moto_data_viewer/venv/bin/activate

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=/home/sanya/moto_data_viewer/core_app.py
flask run --host=0.0.0.0 --port=5002

#cat /dev/# some_bt_device # >> ~/moto_data_viewer/mdu.log
