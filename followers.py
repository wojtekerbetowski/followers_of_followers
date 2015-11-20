# -*- coding: utf-8 -*-
import tweepy
import itertools
from collections import Counter
import os

# Check environment vars
try:
    CONSUMER_KEY        = os.environ["CONSUMER_KEY"]
    CONSUMER_SECRET     = os.environ["CONSUMER_SECRET"]
    ACCESS_TOKEN        = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

except KeyError as k:
    print('ERROR: Missing environment variable: {}. Exiting!'.format(k.message))
    exit()

# connect to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, 
                 cache=tweepy.FileCache('tweepycache', timeout=-1), 
                 wait_on_rate_limit=True, 
                 wait_on_rate_limit_notify=True)

def my_followers():
    return tweepy.Cursor(api.followers, screen_name='erbetowski', count=200).items()

def my_indirect_followers():
    my_followers_list = list(my_followers())
    for i, f in enumerate(my_followers_list):
        print('Loading followers of %s ... ' % f.screen_name),
        for ff in api.followers(screen_name=f.screen_name, count=200):
            yield ff
        print("done. That's {} out of {}".format(i, len(my_followers_list)))

print(Counter((f.screen_name for f in my_indirect_followers())).most_common(30))

