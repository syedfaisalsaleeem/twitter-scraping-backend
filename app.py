from flask import Flask, jsonify,request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.debug = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

@app.route("/twitter", methods=['POST','GET'])
@cross_origin()
def twitter():
    if request.method == 'POST':
        from task_queue import twitter_scraping
        request_data = request.get_json()
        twitter_scraping.apply_async(kwargs={"query":(request_data['key_phrases'], request_data['start_date'], request_data['end_date'], request_data['method'], request_data['break'])})
        return jsonify({"status": "success"})

    elif request.method == 'GET':
        return jsonify({"body":"true"})

# @app.route("/twitter/<keyphrase_id>")
# def get_specific_keyphrase(keyphrase_id):
#     return jsonify({"body":Controller2().get_specific_keyphrase(db, keyphrase_id)})

if __name__ == "__main__":
  app.run(host='localhost', port='8080', debug=False)