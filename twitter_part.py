import sys, tweepy, os, datetime

consumer_key = 'IOLJfJDBoPTMmpe6jqoo9quya'
consumer_secret = 'aKQsEsJe7O3EVJQXgwaQ1O3saHulaAk0jaFndGZMjc2oOVtKNW'
access_token = '1269651960954748930-0i2qXxy9UMHjqYseJyl7SerIOkabbv'
access_secret = 'JSp33pz7py2fy19c3fXzKhTuzdW2xP02W6g8ngcTI3NEl'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api = tweepy.API(auth)

def retrieve_python_weekly():
    for tweet in tweepy.Cursor(api.user_timeline,screen_name='PythonWeekly').items(5):
        if tweet.created_at > datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=4):
            print(f'Posted at {tweet.created_at}')
            print(tweet.text)

def retrieve_real_python():
    for tweet in tweepy.Cursor(api.user_timeline,screen_name='realpython').items(5):
        if tweet.created_at > datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=4):
            print(f'Posted at {tweet.created_at}')
            print(tweet.text)

def retrieve_fullstackpython():
    for tweet in tweepy.Cursor(api.user_timeline,screen_name='fullstackpython').items(5):
        if tweet.created_at > datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(hours=4):
            print(f'Posted at {tweet.created_at}')
            print(tweet.text)


if __name__ == '__main__':
    user = input('Enter username: ')

