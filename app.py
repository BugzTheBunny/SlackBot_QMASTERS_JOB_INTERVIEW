import datetime
import tweepy
import flask
import json
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler

# settings.
super_secret_web_hook = os.environ.get('WEBHOOK')  # Slack Webhook

twitter_consumer_key = 'IOLJfJDBoPTMmpe6jqoo9quya' #os.environ.get('TCK')
twitter_consumer_secret = 'aKQsEsJe7O3EVJQXgwaQ1O3saHulaAk0jaFndGZMjc2oOVtKNW' #os.environ.get('TCS')
twitter_access_token = '1269651960954748930-0i2qXxy9UMHjqYseJyl7SerIOkabbv' #os.environ.get('TAT')
twitter_access_secret = 'JSp33pz7py2fy19c3fXzKhTuzdW2xP02W6g8ngcTI3NEl' #os.environ.get('TAS')

auth = tweepy.OAuthHandler(twitter_consumer_key,twitter_consumer_secret)
auth.set_access_token(twitter_access_token,twitter_access_secret)

api = tweepy.API(auth)
#################### Schedule of sending a message.##############################
def schedule_send_time_request():
    requests.post(super_secret_web_hook, json.dumps({'text': f'{datetime.datetime.now()}'}))


scheduler = BackgroundScheduler()
scheduler.add_job(func=schedule_send_time_request, trigger="interval", seconds=3600)
scheduler.start()


################################################################################

app = flask.Flask(__name__)
# Methods
@app.route('/')
def home():
    requests.post(super_secret_web_hook, json.dumps({'text': f'{datetime.datetime.now()}'}))
    return 'Time sent!'

@app.route('/python-weekly', methods=['POST'])
def retrieve_python_weekly():
    '''
    Python Weekly latests tweets retriever.
    :return: Returns the latest tweets
    '''
    for tweet in tweepy.Cursor(api.user_timeline, screen_name='PythonWeekly').items(5):
        if tweet.created_at > datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=4):
            requests.post(super_secret_web_hook,tweet.text.encode('utf-8'))
    return 'retrieved Python Weekly tweets!'

@app.route('/real-python', methods=['POST'])
def retrieve_real_python():
    '''
    Real Python latests tweets retriever.
    :return: Returns the latest tweets
    '''
    for tweet in tweepy.Cursor(api.user_timeline, screen_name='PythonWeekly').items(5):
        if tweet.created_at > datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=4):
            requests.post(super_secret_web_hook,tweet.text.encode('utf-8'))
    return 'retrieved Real Python tweets!'

@app.route('/python-hub', methods=['POST'])
def retrieve_python_hub():
    '''
    Real Python latests tweets retriever. - Added this one cause it had hourly posts.
    :return: Returns the latest tweets
    '''
    for tweet in tweepy.Cursor(api.user_timeline, screen_name='pythonhub').items(5):
        if tweet.created_at > datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=4):
            requests.post(super_secret_web_hook,tweet.text.encode('utf-8'))
    return 'retrieved Python Hub tweets!'

@app.route('/fullstack-python', methods=['POST'])
def retrieve_fullstackpython():
    '''
    Full Stack Python latests tweets retriever.
    :return: Returns the latest tweets
    '''
    for tweet in tweepy.Cursor(api.user_timeline, screen_name='PythonWeekly').items(5):
        if tweet.created_at > datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=4):
            requests.post(super_secret_web_hook,tweet.text.encode('utf-8'))
    return 'retrieved Full Stack Python  tweets!'

@app.route('/time', methods=['POST'])
def time():
    return f"{datetime.datetime.now()}"


if __name__ == '__main__':
    app.run(debug=True)
