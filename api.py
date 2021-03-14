import flask
from flask import request, jsonify
from threading import Thread
from main import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "The Api Works"

@app.route('/checkproduct', methods=['GET'])
def check_for_product():
    if 'barcode' in request.args:
        barcode = str(request.args['barcode'])
    else:
        return "Error make sure you provide a barcode"
    data = search_database(barcode)
    return jsonify(data)

#app.run(host='0.0.0.0',port=8080)  # For Replit
#app.run()  # For Pycharm