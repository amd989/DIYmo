__author__ = 'Alejandro'
#!flask/bin/python

from pifacedigitalio import PiFaceDigital
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import url_for
from flask import request
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)

switches = [
    {
        'id': 1,
        'title': u'PS3 Controller Charger',
        'description': u'Turns on or off the PS3 Controller Charger',
        'state': False
    },
    {
        'id': 2,
        'title': u'Lava Lamp',
        'description': u'Turns On or Off the Lava Lamp',
        'state': False
    }
]

auth = HTTPBasicAuth()
piFaceDigital = PiFaceDigital()

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


@app.route('/api/v1.0/switches', methods=['GET'])
def get_switches():
    return jsonify({'switches': map(make_public_switch, switches)})


def make_public_switch(switch):
    new_switch = {}
    for field in switch:
        if field == 'id':
            new_switch['uri'] = url_for('get_switch', switch_id=switch['id'], _external=True)
        else:
            new_switch[field] = switch[field]
    return new_switch


@app.route('/api/v1.0/switches/<int:switch_id>', methods=['GET'])
def get_switch(switch_id):
    switch = filter(lambda t: t['id'] == switch_id, switches)
    if len(switch) == 0:
        abort(404)
    return jsonify({'switch': switch[0]})


@app.route('/api/v1.0/switches/toggle/<int:switch_id>', methods=['PUT'])
def toggle_switch(switch_id):
    switch = filter(lambda t: t['id'] == switch_id, switches)
    if len(switch) == 0:
        abort(404)

    outputPin = piFaceDigital.output_pins[switch_id]
    state = switch[0].state
    if state:
        outputPin.turn_off()
    else:
        outputPin.turn_on()

    switch[0].state = not state
    return jsonify({'result': switch[0].state})


@app.route('/api/v1.0/switches', methods=['POST'])
def create_switch():
    if not request.json or not 'title' in request.json:
        abort(400)
    switch = {
        'id': switches[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    switches.append(switch)
    return jsonify({'switch': switch}), 201


@app.route('/api/v1.0/switches/<int:switch_id>', methods=['PUT'])
def update_switch(switch_id):
    switch = filter(lambda t: t['id'] == switch_id, switches)
    if len(switch) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    switch[0]['title'] = request.json.get('title', switch[0]['title'])
    switch[0]['description'] = request.json.get('description', switch[0]['description'])
    switch[0]['done'] = request.json.get('done', switch[0]['done'])
    return jsonify({'switch': switch[0]})


@app.route('/api/v1.0/switches/<int:switch_id>', methods=['DELETE'])
def delete_switch(switch_id):
    switch = filter(lambda t: t['id'] == switch_id, switches)
    if len(switch) == 0:
        abort(404)
    switches.remove(switch[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

if __name__ == '__main__':
    app.run(debug=True)