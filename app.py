from flask import Flask, request, render_template
from flask_cors import CORS
import json
import wda
import tidevice
import time
import os
import re
import subprocess
from logzero import logger

app = Flask(__name__, template_folder='static')
CORS(app, support_crenditals=True, resources={r"/*": {"origins": "*"}}, send_wildcard=True)


def _get_bundle_id():
    t = tidevice.Device()
    target_bundle = ''
    for info in t.installation.iter_installed():
        display_name = info['CFBundleDisplayName']
        if display_name == 'WebDriverAgentRunner-Runner':
            target_bundle = info['CFBundleIdentifier']
            return target_bundle
    if target_bundle == '':
        raise Exception('No Bundle!!!!')


def _get_udid():
    udid = re.findall('\\ "udid\"\\:\\ "(.*?)\"', str(subprocess.Popen(cmds['device_udid'], shell=True, stdout=subprocess.PIPE).communicate()[0]))[0]
    return udid


def connect_device():
    """
    :return: USBClient
    """
    udid = _get_udid()
    bundle_id = _get_bundle_id()
    c = wda.USBClient(udid=udid, wda_bundle_id=bundle_id)
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
    print(disX, disY)
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
    client.home()
    client.orientation = 'PORTRAIT'
    logger.info('Back to home')
    return "back to home"


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
    os.system(f'tidevice screenshot {path}/screenshot/{screenshot_name}.png')
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


@app.route('/send', methods=['POST'])
def send():
    data = json.loads(request.form.get('data'))
    content = data['text']
    client.send_keys(content)
    logger.info('send text content: {}'.format(content))
    return "send text"


if __name__ == '__main__':
    # with open('device.json', 'r', encoding='utf-8') as f:
    #     json_data = json.load(f)
    #     udid = json_data.get('udid')
    #     wda_bundle_id = json_data.get('wda_bundle_id')
    # client = wda.USBClient(
    #     udid=udid,
    #     port=8100,
    #     wda_bundle_id=wda_bundle_id)
    path = os.path.abspath('')
    cmds = {'device_udid': 'tidevice list --json',
            'remote': 'tidevice relay {0} 9100'}
    client = connect_device()
    app.run(debug=True)