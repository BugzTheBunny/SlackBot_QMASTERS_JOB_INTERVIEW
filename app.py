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
auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)  # Twitter auth handler
auth.set_access_token(twitter_access_token, twitter_access_secret)  # Setting access Token
api = tweepy.API(auth)  # connection to Twitter API.

user_id = '1269651960954748930'  # The ID of the user that the bot will follow, and get his latest updates.
run_stream_with_user = False  # This handles the Streaming (Getting updates on new tweets)


def schedule_send_time_request():
    """
    Makes the bot to send an update every period of time (Set by user above).
    :return:
    """
    requests.post(
        super_secret_web_hook,
        json.dumps({'text': f'> :robot_face::speech_balloon:*  Latest Updates:* *Time: {datetime.datetime.now()}*'}))
    send_update('PythonWeekly', 'Python Weekly')
    send_update('RealPython', 'Real Python')
    send_update('PythonWeekly', 'Python Weekly')


scheduler = BackgroundScheduler()
scheduler.add_job(func=schedule_send_time_request, trigger="interval", seconds=seconds_interval_per_update)
scheduler.start()

if run_stream_with_user:
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


    """
    This won't work on Heroku free account, this WILL work locally, or on a proper server.
    change to True to make it work locally, this starts the Streaming (Following) for the user account, and gives you
    instant updates on new tweets from the selected user.
    """
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(follow=[user_id])


def send_update(username, user_full_name):
    """
    The 'hours=4' is set like this, because of the time differences, it's actually 1 hour ago.
    :param user_full_name: full name of the user
    :param username: Name of the account from which we want the latest tweets.

    :return:
    """
    try:
        response = ''
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items(5):
            if tweet.created_at > datetime.datetime.now() - datetime.timedelta(hours=latest_tweets_time):
                response = response + f'*•* {tweet.text} \n\n'
        if response != '':
            requests.post(super_secret_web_hook,
                          json.dumps({"text": f'>:robot_face::speech_balloon: *News from {user_full_name}!*'}))
            requests.post(super_secret_web_hook, json.dumps({"text": f'{response}'}))
        logging.info('Sent an update!')
        return f'{username} News!:'
    except:
        logging.error("Something is wrong with sending a message")
        return False


@app.route('/python-weekly', methods=['POST'])
def retrieve_python_weekly():
    try:
        send_update('PythonWeekly', 'Python Weekly')
        return True
    except:
        logging.error("Something is wrong with '/python-weekly'")
        return False

@app.route('/real-python', methods=['POST'])
def retrieve_real_python():
    try:
        send_update('RealPython', 'Real Python')
        return True
    except:
        logging.error("Something is wrong with '/real-python'")
        return False

@app.route('/python-hub', methods=['POST'])
def retrieve_python_hub():
    try:
        send_update('PythonHub', 'Python Hub')
        return True
    except:
        logging.error("Something is wrong with '/python-hub'")
        return False

@app.route('/fullstack-python', methods=['POST'])
def retrieve_fullstackpython():
    try:
        send_update('fullstackpython', 'Full Stack Python')
        return True
    except:
        logging.error("Something is wrong with '/fullstack-python'")
        return False

@app.route('/csharpstack', methods=['POST'])
def retrieve_csharpstack():
    try:
        send_update('csharpstack','C# StackOverflow')
        return True
    except:
        logging.error("Something is wrong with '/csharpstack'")
        return False

@app.route('/javascriptdaily', methods=['POST'])
def retrieve_javascriptdaily():
    try:
        send_update('JavaScriptDaily', 'JavaScript Daily')
        return True
    except:
        logging.error("Something is wrong with '/javascriptdaily'")
        return False
@app.route('/cprogramming1', methods=['POST'])
def retrieve_cprogramming1():
    try:
        send_update('CProgramming1','C++ Programming')
        return True
    except:
        logging.error("Something is wrong with '/cprogramming1'")
        return False

@app.route('/updates', methods=['POST'])
def get_updates():
    try:
        schedule_send_time_request()
        return True
    except:
        logging.error("Something is wrong with '/updates'")
        return False

@app.route('/tweet', methods=['POST'])
def post_tweet():
    try:
        api.update_status(flask.request.data)
        return True
    except:
        logging.error("Something is wrong with '/tweet'")
        return False

@app.route('/time', methods=['POST'])
def time():
    try:
        requests.post(super_secret_web_hook, json.dumps({'text': f' Current time: *{datetime.datetime.now()}*'}))
        return True
    except:
        logging.error("Something is wrong with '/time'")
        return False

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
