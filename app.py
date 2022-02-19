from flask import Flask, jsonify,request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from pymongo import MongoClient
from authentication_controller import AuthenticationController
from extensions import register_extensions
import os
from datetime import timedelta

app = Flask(__name__)
app.debug = True
app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

register_extensions(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

client = MongoClient("mongodb://localhost:27017/")
db = client['authentication']
try:
    auth = AuthenticationController(db).register(username="admin",password="cryptography")
    print(auth)
except Exception as e:
    print("error",e)

@app.route("/twitter", methods=['POST','GET'])
@jwt_required()
def twitter():
    if request.method == 'POST':
        from task_queue import twitter_scraping
        request_data = request.get_json()
        twitter_scraping.apply_async(kwargs={"query":(request_data['key_phrases'], request_data['start_date'], request_data['end_date'], request_data['method'], request_data['break'])})       
        return jsonify({"status": "success"})

    elif request.method == 'GET':
        return jsonify({"body":"true"})

@app.route("/login", methods=['POST'])
def login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    auth = AuthenticationController(db).login(username=username,password=password)
    return auth

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='8080', debug=True)