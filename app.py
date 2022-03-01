from flask import Flask, jsonify,request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from pymongo import MongoClient
from application.app.cronjob.controllers.control_cronjob_controller import ControlCronJobController
from authentication_controller import AuthenticationController
from extensions import register_extensions
import os
from datetime import timedelta
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.debug = True
app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

register_extensions(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['TIMEZONE'] = 'UTC'

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

client = MongoClient("mongodb://localhost:27017/")
db = client['authentication']
db_twitter = client['twitter']
try:
    auth = AuthenticationController(db).register(username="admin",password="cryptography")
    print(auth)
except Exception as e:
    print("error",e)
try:
    cronjob_controller = ControlCronJobController(db_twitter)
    response = cronjob_controller.insert()
except Exception as e:
    print("error",e)

@app.route("/twitter", methods=['POST','GET'])
@jwt_required(refresh=True)
def twitter():
    if request.method == 'POST':
        from task_queue import twitter_scraping
        request_data = request.get_json()
        twitter_scraping.apply_async(kwargs={"query":(request_data['key_phrases'], request_data['start_date'], request_data['end_date'], request_data['method'], request_data['break'])},queue='generic')       
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


@app.route("/notification", methods=["GET","PUT"])
@jwt_required(refresh=True)
def notification():
    if request.method == "GET":
        from application.app.notification.notification_controller import NotificationController
        args = request.args
        status = args.get("status", type=str)
        notification_controller = NotificationController(db_twitter)
        notification_controller.delete_keyphrase()
        data = notification_controller.get_all_keyphrases(status=status)
        return data

    if request.method == "PUT":
        request_data = request.get_json()
        method = request_data['method']
        from application.app.notification.notification_controller import NotificationController
        notification_controller = NotificationController(db_twitter)
        response = notification_controller.update_keyphrase(method)
        return response

@app.route("/cronjob", methods=["GET","POST","DELETE"])
@jwt_required(refresh=True)
def cronjob():
    if request.method == "GET":
        from application.app.cronjob.controllers.cronjob_controller import CronJobController
        args = request.args
        status = args.get("status", type=str)
        cronjob_controller = CronJobController(db_twitter)
        response = cronjob_controller.get_all_keyphrases("cronjob")
        return response

    if request.method == "POST":
        from application.app.cronjob.controllers.cronjob_controller import CronJobController
        request_data = request.get_json()
        keyphrases = request_data['keyphrases']
        cronjob_controller = CronJobController(db_twitter)
        response = cronjob_controller.insert_cronjob_keyphrase(keyphrases)
        return response
    
    if request.method == "DELETE":
        from application.app.cronjob.controllers.cronjob_controller import CronJobController
        request_data = request.get_json()
        _id = request_data['id']
        cronjob_controller = CronJobController(db_twitter)
        response = cronjob_controller.delete_cronjob_keyphrase(_id)
        return response

@app.route("/controlcronjob", methods=["GET","PUT"])
@jwt_required(refresh=True)
def controlcronjob():
    if request.method == "GET":
        from application.app.cronjob.controllers.control_cronjob_controller import ControlCronJobController
        control_cronjob_controller = ControlCronJobController(db_twitter)
        response = control_cronjob_controller.get()
        return response

    if request.method == "PUT":
        from application.app.cronjob.controllers.control_cronjob_controller import ControlCronJobController
        request_data = request.get_json()
        status = request_data['status']
        control_cronjob_controller = ControlCronJobController(db_twitter)
        response = control_cronjob_controller.update(status)
        return response

if __name__ == "__main__":
  app.run(host='0.0.0.0', port='8080', debug=True)