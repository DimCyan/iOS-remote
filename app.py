from flask import Flask, request, render_template
from flask_cors import *
import json

app = Flask(__name__, template_folder='static')
CORS(app, support_crenditals=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/click', methods=['POST'])
def click():
    data = json.loads(request.form.get('data'))
    disX = data['disX']
    disY = data['disY']
    print('click: ({}, {})'.format(disX, disY))
    return "click it"


@app.route('/drag', methods=['POST'])
def drag():
    data = json.loads(request.form.get('data'))
    disX = data['disX']
    disY = data['disY']
    toX = data['toX']
    toY = data['toY']
    print('click: ({}, {}) and drag to: ({}, {})'.format(disX, disY, toX, toY))
    return "click and drag it"


if __name__ == '__main__':
    app.run(debug=True)