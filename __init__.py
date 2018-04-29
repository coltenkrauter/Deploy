from flask import Flask,jsonify,request
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS (Cross Origin Resource Sharing) in order to for swagger doc to work
CORS(app)

from . import endpoints

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)