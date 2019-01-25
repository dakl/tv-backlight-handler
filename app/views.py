import structlog
from colour import Color
from flask import abort, jsonify, request

from app.accessories import ACCESSORIES
from app.setup import app

logger = structlog.getLogger(__name__)

HEADERS = {"Content-type": "application/x-www-form-urlencoded"}
STATE_MAP = {'on': 1, 'off': 0}


@app.route('/')
def health():

    return jsonify({'status': 'up', 'message': 'Service is healthy.'})


@app.route('/api/v1/accessories', methods=['GET'])
def list_accessories():
    accessories = [{
        'id': accessory_id,
        'name': accessory.name
    } for accessory_id, accessory in ACCESSORIES.items()]
    return jsonify({'accessories': accessories})


@app.route('/api/v1/accessories/<int:accessory_id>/status', methods=['POST'])
def set_status(accessory_id):
    if accessory_id not in ACCESSORIES:
        abort(404)
    raw_state = request.json.get('value')
    state = STATE_MAP.get(raw_state)
    accessory = ACCESSORIES.get(accessory_id)
    new_state = accessory.set_status(state)
    return jsonify({'id': accessory_id, 'new_state': new_state})


@app.route('/api/v1/accessories/<int:accessory_id>/status', methods=['GET'])
def get_status(accessory_id):
    if accessory_id not in ACCESSORIES:
        abort(404)

    accessory = ACCESSORIES.get(accessory_id)
    return str(accessory.get_status())


@app.route(
    '/api/v1/accessories/<int:accessory_id>/brightness', methods=['POST'])
def set_brightness(accessory_id):
    if accessory_id not in ACCESSORIES:
        abort(404)
    value = int(request.json.get('value'))
    if value < 0 or value > 100:
        abort(400)
    accessory = ACCESSORIES.get(accessory_id)
    new_value = accessory.set_brightness(value)
    return jsonify({'id': accessory_id, 'new_brightness': new_value})


@app.route(
    '/api/v1/accessories/<int:accessory_id>/brightness', methods=['GET'])
def get_brightness(accessory_id):
    if accessory_id not in ACCESSORIES:
        abort(404)

    accessory = ACCESSORIES.get(accessory_id)
    return str(accessory.get_brightness())


@app.route('/api/v1/accessories/<int:accessory_id>/color', methods=['POST'])
def set_color(accessory_id):
    if accessory_id not in ACCESSORIES:
        abort(404)
    value = request.json.get('value')
    try:
        color = Color(f'#{value}')
    except Exception:
        abort(400)

    accessory = ACCESSORIES.get(accessory_id)
    accessory.set_color(
        int(255 * color.red), int(255 * color.green), int(255 * color.blue))
    return jsonify({'id': accessory_id, 'new_color': f'#{value}'})


@app.route('/api/v1/accessories/<int:accessory_id>/color', methods=['GET'])
def get_color(accessory_id):
    if accessory_id not in ACCESSORIES:
        abort(404)

    accessory = ACCESSORIES.get(accessory_id)

    r, g, b = accessory.get_color()
    try:
        color = Color(r=r / 255, g=g / 255, b=b / 255)
    except Exception:
        abort(400)

    return color.hex_l.replace('#', '')
