import datetime
import tweepy
import flask
import json
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler

# settings.
super_secret_web_hook = os.environ.get('WEBHOOK')  # Slack Webhook

twitter_consumer_key = os.environ.get('TCK')
twitter_consumer_secret = os.environ.get('TCS')
twitter_access_token = os.environ.get('TAT')
twitter_access_secret = os.environ.get('TAS')

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

api = tweepy.API(auth)

app = flask.Flask(__name__)


def schedule_send_time_request():
    """
    Sends a message to the slack bot every period of time.
    :return:
    """
    requests.post(super_secret_web_hook, json.dumps({'text': f'{datetime.datetime.now()}'}))


scheduler = BackgroundScheduler()
scheduler.add_job(func=schedule_send_time_request, trigger="interval", seconds=3600)
scheduler.start()


def send_update(username):
    """
    The 'hours=4' is set like this, because of the time differences, it's actually 1 hour ago.
    :param username: Name of the account from which we want the latest tweets.

    :return:
    """
    requests.post(
        super_secret_web_hook,
        json.dumps({"text": f"> :robot_face::speech_balloon:*  Latest news from {username} !! BEEP*"}))
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items(5):
        if tweet.created_at > datetime.datetime.now() - datetime.timedelta(hours=4):
            requests.post(super_secret_web_hook, json.dumps({"text": f'{tweet.text}'}))
            requests.post(super_secret_web_hook, json.dumps({"text": f' '}))
    requests.post(super_secret_web_hook, json.dumps({"text": "> :robot_face::speech_balloon: *Well, that's it!*"}))
    return f'{username} News!:'


@app.route('/python-weekly', methods=['POST'])
def retrieve_python_weekly():
    send_update('PythonWeekly')
    return flask.Response()


@app.route('/real-python', methods=['POST'])
def retrieve_real_python():
    send_update('RealPython')
    return flask.Response()

@app.route('/python-hub', methods=['POST'])
def retrieve_python_hub():
    send_update('PythonHub')
    return flask.Response()

@app.route('/fullstack-python', methods=['POST'])
def retrieve_fullstackpython():
    send_update('PythonWeekly')
    return flask.Response()

@app.route('/time', methods=['POST'])
def time():
    requests.post(super_secret_web_hook, json.dumps({'text': f'{datetime.datetime.now()}'}))
    return flask.Response()


if __name__ == '__main__':
    app.run(debug=True)
