import datetime
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import flask
import json
import os
import requests
import logging
from apscheduler.schedulers.background import BackgroundScheduler

# Global settings.
logging.basicConfig(filename='LOGGER.log', level=logging.DEBUG)  # Logger
super_secret_web_hook = os.environ.get('WEBHOOK')  # Slack Webhook
seconds_interval_per_update = 3600  # Time interval per update
latest_tweets_time = 5  # The time from where we want tweets(1 hour ago, means 4 hours ago because of time diffs in IL).
app = flask.Flask(__name__)  # Flask App

# Twitter Settings
twitter_consumer_key = os.environ.get('TCK')  # Consumer Key
twitter_consumer_secret = os.environ.get('TCS')  # Consumer Secret
twitter_access_token = os.environ.get('TAT')  # Access Token
twitter_access_secret = os.environ.get('TAS')  # Access Secret
auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)   # Twitter auth handler
auth.set_access_token(twitter_access_token, twitter_access_secret)  # Setting access Token
user_id = '1269651960954748930'  # The ID of the user that the bot will follow, and get his latest updates.
api = tweepy.API(auth)  # connection to Twitter API.


# def schedule_send_time_request():
#     """
#     Makes the bot to send an update every period of time (Set by user above).
#     :return:
#     """
#     requests.post(
#         super_secret_web_hook,
#         json.dumps({'text': f'> :robot_face::speech_balloon:*  Latest Updates:* *Time: {datetime.datetime.now()}*'}))
#     send_update('PythonWeekly')
#     send_update('RealPython')
#     send_update('PythonWeekly')
#
#
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=schedule_send_time_request, trigger="interval", seconds=seconds_interval_per_update)
# scheduler.start()

class TwitterListener(StreamListener):
    def on_data(self, data):
        try:
            data = json.loads(data)
            requests.post(super_secret_web_hook, json.dumps({"text": f'{data["text"]}'}))
            logging.info(f'User has posted an update : {data["text"]}')
            return True
        except:
            logging.error(f'There was no data while following the user.')
    def on_error(self, status_code):
        logging.warning(f'Something went wrong while following Twitter.{status_code}')


listener = TwitterListener()
stream = Stream(auth, listener)
stream.filter(follow=[user_id])

def send_update(username):
    """
    The 'hours=4' is set like this, because of the time differences, it's actually 1 hour ago.
    :param username: Name of the account from which we want the latest tweets.

    :return:
    """
    response = ''
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items(5):
        if tweet.created_at > datetime.datetime.now() - datetime.timedelta(hours=latest_tweets_time):
            response = response + f'*•* {tweet.text} \n\n'
    if response != '':
        requests.post(super_secret_web_hook,
                      json.dumps({"text": f'>:robot_face::speech_balloon: *News from {username}!*'}))
        requests.post(super_secret_web_hook, json.dumps({"text": f'{response}'}))
    logging.info('Sent an update!')
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


@app.route('/updates', methods=['POST'])
def get_updates():
    schedule_send_time_request()
    return flask.Response()


@app.route('/time', methods=['POST'])
def time():
    requests.post(super_secret_web_hook, json.dumps({'text': f' Current time: *{datetime.datetime.now()}*'}))
    logging.info('Sent an time!')
    return flask.Response()




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
