import os
import tweepy
import json
from pprint import pprint
import sys
from tweet_auth2 import Twitter_user
#print(sys.path)

# fetch the secrets from our virtual environment variables
CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

# authenticate to the service we're accessing
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# create the connection
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
tweets = tweepy.Cursor(api.search,
         q="python",
         lang="en",
         since=2018-11-16).items(5)
screenname_list = []
follower_list = []
for tweet in tweets:
    screenname_list.append(tweet.user.screen_name)
    follower_list.append(tweet.user.followers_count)
    #print(f"{tweet.user.screen_name} AND {tweet.text} AND {tweet.created_at}")
print(follower_list)


# for i in screenname_list:
#     x = Twitter_user(i)
#     print(f"{i} has {x.avg_len()} character tweets" )
#     print(f"{i} has {x.longest_word()} in tweet" )
#     x.num_follow()

avg_num_followers = sum(follower_list) / len(follower_list)
print(f"The average number of followers are {avg_num_followers}")
