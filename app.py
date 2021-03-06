from flask import Flask, request, render_template
from flask_cors import CORS
import json
import wda
import tidevice
import time
import os
import subprocess
from logzero import logger

app = Flask(__name__, template_folder='static')
CORS(app, support_crenditals=True, resources={r"/*": {"origins": "*"}}, send_wildcard=True)


def _get_bundle_id():
    target_bundle = ''
    for info in device.installation.iter_installed():
        display_name = info['CFBundleDisplayName']
        if display_name == 'WebDriverAgentRunner-Runner':
            target_bundle = info['CFBundleIdentifier']
            return target_bundle
    if target_bundle == '':
        raise Exception('No Bundle!!!!')


def connect_device():
    bundle_id = _get_bundle_id()
    c = wda.USBClient(wda_bundle_id=bundle_id)
    return c


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/remote', methods=['POST'])
def remote():
    data = json.loads(request.form.get('data'))
    content = data['text']
    logger.info('remote to: {}'.format(content))
    subprocess.Popen(cmds['remote'].format(content), shell=True, stdout=subprocess.PIPE).communicate()
    return "remote screen"


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
    logger.info('drag: ({}, {}) and drag to: ({}, {})'.format(disX, disY, toX, toY))
    return "click and drag it"


@app.route('/home', methods=['POST'])
def home():
    device.instruments.app_launch('com.apple.springboard')
    client.orientation = 'PORTRAIT'
    logger.info('Back to home')
    return "click home button"


@app.route('/backspace', methods=['POST'])
def backspace():
    client.send_keys('\b')
    logger.info('Click backspace')
    return "click backspace"


@app.route('/enter', methods=['POST'])
def enter():
    client.send_keys('\n')
    logger.info('Click enter')
    return "click enter"


@app.route('/lock', methods=['POST'])
def lock():
    client.lock()
    logger.info('Press lock button to lock/unlock')
    return "press lock button"


@app.route('/screenshot', methods=['POST'])
def screenshot():
    screenshot_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    device.screenshot().convert("RGB").save(f'{path}/screenshot/{screenshot_name}.png')
    # os.system(f'tidevice screenshot {path}/screenshot/{screenshot_name}.png')
    logger.info('Press screenshot button to screenshot')
    return "press screenshot button"


@app.route('/rotation', methods=['POST'])
def rotation():
    orientation = client.orientation
    if orientation == 'PORTRAIT':
        client.orientation = 'LANDSCAPE'
    else:
        client.orientation = 'PORTRAIT'
    logger.info('Switch orientation')
    return "switch orientation"


@app.route('/reboot', methods=['POST'])
def reboot():
    device.reboot()
    logger.info('Press reboot button to reboot')
    return "press reboot button"


@app.route('/send', methods=['POST'])
def send():
    data = json.loads(request.form.get('data'))
    content = data['text']
    client.send_keys(content)
    logger.info('send text content: {}'.format(content))
    return "send text"


if __name__ == '__main__':
    path = os.path.abspath('')
    cmds = {'remote': 'tidevice relay {0} 9100'}
    device = tidevice.Device()
    # um = tidevice.Usbmux()
    # device_udid_list = um.device_udid_list()
    client = connect_device()
    app.run(debug=True)