from flask import Flask, request, render_template
from flask_cors import *
import json
import wda
from logzero import logger

app = Flask(__name__, template_folder='static')
CORS(app, support_crenditals=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/click', methods=['POST'])
def click():
    data = json.loads(request.form.get('data'))
    disX = float(data['disX'])
    disY = float(data['disY'])
    client.click(disX, disY)
    logger.info('click: ({}, {})'.format(disX, disY))
    return "click it"


@app.route('/drag', methods=['POST'])
def drag():
    data = json.loads(request.form.get('data'))
    disX = float(data['disX'])
    disY = float(data['disY'])
    toX = float(data['toX'])
    toY = float(data['toY'])
    client.swipe(x1=disX, y1=disY, x2=toX, y2=toY, duration=0)
    logger.info('click: ({}, {}) and drag to: ({}, {})'.format(disX, disY, toX, toY))
    return "click and drag it"


@app.route('/home', methods=['POST'])
def home():
    client.home()
    logger.info('Back to home')
    return "back to home"


@app.route('/lock', methods=['POST'])
def lock():
    client.lock()
    logger.info('Press lock button to lock/unlock')
    return "press lock button"


@app.route('/rotation', methods=['POST'])
def rotation():
    orientation = client.orientation
    if orientation == 'PORTRAIT':
        client.orientation = 'LANDSCAPE'
    else:
        client.orientation = 'PORTRAIT'
    logger.info('Switch orientation')
    return "switch orientation"


@app.route('/send', methods=['POST'])
def send():
    data = json.loads(request.form.get('data'))
    content = data['text']
    client.send_keys(content)
    logger.info('send text content: {}'.format(content))
    return "send text"


if __name__ == '__main__':
    with open('device.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        udid = json_data.get('udid')
        wda_bundle_id = json_data.get('wda_bundle_id')
    client = wda.USBClient(
        udid=udid,
        port=8100,
        wda_bundle_id=wda_bundle_id)
    app.run(debug=True)
