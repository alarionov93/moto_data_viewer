import os
import json
from flask import Flask
from flask import render_template
from flask import request, jsonify
import models
from log_parser import LogParser

app = Flask(__name__)

LAST_MEASURES_VALUE = 10

@app.route('/')
def index():
    measures = models.Measures.select().order_by(models.Measures.measure_id.desc())
    measures_ids = []
    for m in measures:
        measures_ids.append(m.measure_id)

    without_repeates = list(set(measures_ids))
    without_repeates.reverse()
    cutted = without_repeates[:LAST_MEASURES_VALUE]

    return render_template('index.html', measures_ids=cutted)

@app.route('/get_tracker_chg_info/<int:m_id>')
def get_gps_chg_info(m_id):
    if m_id is None:
        raise AttributeError("Measure id is None")
    data = models.Measures.select().where(models.Measures.measure_id == int(m_id)).order_by(models.Measures.created_at)
    data_lst = []
    data_lst.append(['Id', 'Charging Status', 'Charging Percent'])
    for d in data:
        data_lst.append(d.tracker_chg_info_to_list())
    return jsonify(data_lst)

@app.route('/get_measures/<int:m_id>')
def get_measures(m_id):
    if m_id is None:
        raise AttributeError("Measure id is None")
    else:
        measures = models.Measures.select().where(models.Measures.measure_id == int(m_id)).order_by(models.Measures.id)

    measures_lst = []
    measures_lst.append(['Id', 'Temperature Outside', 'Engine Temperature', 'Pressure', 'Voltage', 'Fuel level'])
    for m in measures:
        measures_lst.append(m.to_list())
    # lp = LogParser()
    # lp.parse()
    return jsonify(measures_lst)

@app.route('/update_measures/<int:m_id>')
@app.route('/update_measures/<int:m_id>/<is_new_measure>')
def update_measures(m_id, is_new_measure=False):
    if m_id is None:
        raise AttributeError("Measure id is None")
    else:
        measures = models.Measures.select().where(models.Measures.measure_id == int(m_id)).order_by(models.Measures.id)

    measures_lst = []
    measures_lst.append(['Id', 'Temperature Outside', 'Engine Temperature', 'Pressure', 'Voltage', 'Fuel level'])
    for m in measures:
        measures_lst.append(m.to_list())
    lp = LogParser()
    if int(is_new_measure) == 1:
        lp.parse(truncate_log=True, new_measure=True)
    else:
        lp.parse(truncate_log=True)

    return jsonify(measures_lst)

