import flask
from datetime import datetime
import requests
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler

# settings.
super_secret_web_hook = os.environ.get('WEBHOOK')


################################################################################
# Schedule of sending a message.##############################
def schedule_send_time_request():
    requests.post(super_secret_web_hook, json.dumps({'text': f'{datetime.now()}'}))


scheduler = BackgroundScheduler()
scheduler.add_job(func=schedule_send_time_request, trigger="interval", seconds=600)
scheduler.start()

app = flask.Flask(__name__)
app.config["DEBUG"] = True
################################################################################

# Methods
@app.route('/')
def home():
    requests.post(super_secret_web_hook, json.dumps({'text': f'{datetime.now()}'}))
    return 'Time sent!'


@app.route('/time', methods=['POST'])
def time():
    return f"{datetime.now()}"


if __name__ == '__main__':
    app.run(debug=True)
