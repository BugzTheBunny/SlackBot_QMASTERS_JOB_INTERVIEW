import requests
#  This is the test file - just run it, and put a tweet you want.
#  You will be able to view the new tweet here - https://twitter.com/BugzTheBunny1

new_tweet = input('Post a new tweet:')
requests.post('http://127.0.0.1:5000/tweet', new_tweet)