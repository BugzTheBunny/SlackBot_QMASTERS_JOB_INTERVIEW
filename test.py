from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import tweepy
import os

twitter_consumer_key = os.environ.get('TCK')
twitter_consumer_secret = os.environ.get('TCS')
twitter_access_token = os.environ.get('TAT')
twitter_access_secret = os.environ.get('TAS')

auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

auth.secure = True

api = tweepy.API(auth)

class TwitterListener(StreamListener):
    def on_data(self,data):
        print(data)
        return True
    def on_error(self, status_code):
        print(status_code)

if __name__ == '__main__':
    listener = TwitterListener()

    stream = Stream(auth, listener)
    stream.filter(follow=['1269651960954748930']).items(5)
