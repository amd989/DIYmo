from models import Switch
from time import sleep

__author__ = 'Alejandro'
#!flask/bin/python

from pifacedigitalio import PiFaceDigital
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import url_for
from flask import request
from flask.ext.cors import CORS
from flask.ext.httpauth import HTTPBasicAuth

# configuration
SECRET_KEY = 'da96faab-fe57-4bfb-b433-5edff2f1587f'

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DIYmo_SETTINGS', silent=True)

# Set CORS options on app configuration
# app.config['CORS_HEADERS'] = "Content-Type"
# app.config['CORS_RESOURCES'] = {r"/api/*": {"origins": "*"}}
# cors = CORS(app)
auth = HTTPBasicAuth()
piFaceDigital = PiFaceDigital()
pinMap = { 1 : 0, 2 : 2, 3 : 4, 4 : 6, 5 : 8 }      

@auth.get_password
def get_password(username):
    if username == 'alejandro':
        return 'alex989'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/')
@auth.login_required
def index():
    return "DIYmo, (deemo)"


@app.route('/api/v1/switches', methods=['GET'])
@auth.login_required
def get_switches():
    return jsonify({'switches': map(make_public_switch, Switch.select())})


def make_public_switch(switch):
    new_switch = switch.json()
    new_switch['uri'] = url_for('get_switch', switch_id=switch.id, _external=True)
    return new_switch


@app.route('/api/v1/switches/<int:switch_id>', methods=['GET'])
@auth.login_required
def get_switch(switch_id):
    try:
        switch = Switch.get(Switch.id == switch_id)
    except Switch.DoesNotExists:
        switch = None

    if switch is None:
        abort(404)

    return jsonify({'switch': make_public_switch(switch)})


@app.route('/api/v1/switches/toggle/<int:switch_id>', methods=['PUT'])
@auth.login_required
def toggle_switch(switch_id):
    try:
        switch = Switch.get(Switch.id == switch_id)
    except Switch.DoesNotExists:
        switch = None

    if switch is None:
        abort(404)
    
    switch_piface(switch)    
    switch.state = not state
    switch.save()
    return jsonify({'state': switch.state})


@app.route('/api/v1/switches', methods=['POST'])
@auth.login_required
def create_switch():
    if not request.json or not 'title' in request.json:
        abort(400)

    switch = Switch.create(title=request.json['title'],
                           description=request.json.get('description', ""),
                           state=False,
                           pin=request.json['pin'])
    return jsonify({'switch': make_public_switch(switch)}), 201


@app.route('/api/v1/switches/<int:switch_id>', methods=['PUT'])
@auth.login_required
def update_switch(switch_id):
    try:
        switch = Switch.get(Switch.id == switch_id)
    except Switch.DoesNotExists:
        switch = None

    if switch is None:
        abort(404)
    # if not request.json:
    #     abort(400)
    # if 'title' in request.json and type(request.json['title']) is not unicode:
    #     abort(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode:
    #     abort(400)
    # if 'pin' in request.json and type(request.json['pin']) is not unicode:
    #     abort(400)
    # if 'state' in request.json and type(request.json['state']) is not bool:
    #     abort(400)

    switch.title = request.json.get('title', switch.title)
    switch.description = request.json.get('description', switch.description)
    switch.pin = request.json.get('pin', switch.pin)
    
    switchState = request.json.get('state', switch.state)
    
    if(switchState = not switch.state)
        switch_piface(switch)   
    
    switch.state = switchState
    switch.save()
    return jsonify({'switch': make_public_switch(switch)})


@app.route('/api/v1/switches/<int:switch_id>', methods=['DELETE'])
@auth.login_required
def delete_switch(switch_id):
    try:
        switch = Switch.get(Switch.id == switch_id)
    except Switch.DoesNotExists:
        switch = None

    if switch is None:
        abort(404)

    switch.delete_instance()
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


def switch_piface(switch)
    pinOn = piFaceDigital.output_pins[pinMap[switch.pin]]
    pinOff = piFaceDigital.output_pins[pinMap[switch.pin] + 1]
    state = switch.state
    if state:
        pinOff.turn_on()
        sleep(0.5)
        pinOff.turn_off()
    else:
        pinOn.turn_on()
        sleep(0.1)
        pinOn.turn_off()

if __name__ == '__main__':
    # app.run(host='127.0.0.1')
    # app.run(debug=True)
    app.run(host='0.0.0.0')