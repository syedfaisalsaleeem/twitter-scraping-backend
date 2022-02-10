from flask import Flask, jsonify,request
from controller import Controller, Controller2
from pymongo import MongoClient
from flask_cors import CORS, cross_origin

client = MongoClient("mongodb://localhost:27017/")
db = client['database']

app = Flask(__name__)
app.debug = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/twitter", methods=['POST','GET'])
def twitter():
    if request.method == 'POST':
        request_data = request.get_json()
        response = Controller(request_data['key_phrases'], request_data['start_date'], request_data['end_date'],db).start()
        return jsonify({"status": response[0]})

    elif request.method == 'GET':
        return jsonify({"body":Controller2().get_twitter(db)})

@app.route("/twitter/<keyphrase_id>")
def get_specific_keyphrase(keyphrase_id):
    return jsonify({"body":Controller2().get_specific_keyphrase(db, keyphrase_id)})

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='8080', debug=False)