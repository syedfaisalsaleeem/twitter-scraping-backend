from msilib.schema import Control
from flask import Flask, jsonify,request
from controller import Controller
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client['database']

app = Flask(__name__)
app.debug = True
@app.route("/", methods=['POST'])
def hello():
    request_data = request.get_json()
    response = Controller(request_data['key_phrases'], request_data['start_date'], request_data['end_date'],db).start()
    return jsonify({"status": response[0]})

if __name__ == "__main__":
  app.run()