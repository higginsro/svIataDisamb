from flask import Flask, jsonify
from flask_restful import Api, output_json
from Utilities.RDRPOSTagger.pSCRDRtagger import RDRPOSTagger as tagger


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
