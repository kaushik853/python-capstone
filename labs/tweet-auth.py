import os
import tweepy
from pprint import pprint
import json
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
# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")
# define a handle to inspect for quicker reference
# handle = 'rakyll' # for example purposes; prop any handle you want!
# user = api.get_user(handle)
# #num_friends = user.friends_count
# print(user.name)
# print(num_friends)
# for tweet in tweepy.Cursor(api.user_timeline).items(20):
#     # Process a single status
#     print(tweet.text)
#api.update_status("Hello Tweepy")
# timeline = api.home_timeline()
# for tweet in timeline:
#     print(f"{tweet.user.name} said {tweet.text}")
'''timeline2 = api.user_timeline(screen_name='Kaushik0106')
for tweet in timeline2:
    print(f"{tweet.id} said {tweet.text}")'''
# destroy_id = [1148844793704910849, 1146514958932463616, 1145943875934195712]
# for i in destroy_id:
#     api.destroy_status(id=i)
# user = api.get_user("Kaushik0106")
#
# print("User details:")
# print(user.name)
# print(user.description)
# print(user.location)

# print("Last 20 Followers:")
# for follower in user.followers():
#     print(follower.name)
'''tweets = api.home_timeline(count=1)
tweet = tweets[0]
print(f"Liking tweet {tweet.id} of {tweet.author.name}")
api.create_favorite(tweet.id)'''

# for tweet in api.search(q="Python", lang="en", rpp=10):
#     print(f"{tweet.user.name}:{tweet.text}")

# trend_list = api.trends_available()
# pprint(trend_list)

# trends_result = api.trends_place(1)
# for trend in trends_result[0]["trends"]:
#     pprint(trend["name"])

# for status in tweepy.Cursor(api.user_timeline, id='rakyll').items(1):
#     print(status)
followers = api.followers(screen_name='rakyll')
followers_list = []
for i in followers:
    # pprint(tweet._json)  # uncomment to see the tweet data
    followers_list.append(i._json)

with open('rakyll_follower.json', 'w') as f:
    json.dump(followers_list, f)
