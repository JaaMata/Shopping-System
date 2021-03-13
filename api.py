import flask
from flask import request, jsonify
from main import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "hello"

@app.route('/checkproduct', methods=['GET'])
def check_for_product():
    if 'barcode' in request.args:
        barcode = str(request.args['barcode'])
    else:
        return "Error make sure you provide a barcode"
    data = search_database(barcode)
    return jsonify(data)
app.run()