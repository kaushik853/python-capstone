import os
import tweepy
import json
from pprint import pprint


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


class Twitter_user:
    def __init__(self, handle):
        self.handle = handle
        self.tweets = api.user_timeline(screen_name=self.handle)
        self.tweet_list = []
        for tweet in self.tweets:
            self.tweet_list.append(tweet.text)

    def avg_len(self):
        tweet_words = []
        tweet_character = []
        for tweet in self.tweet_list:
          words = tweet.split()
          tweet_words.append(len(words))
          for word in words:
              tweet_character.append(len(word))
        return sum(tweet_character) / len(tweet_words)

    def longest_word(self):
        i = 1
        k = {}
        for tweet in self.tweet_list:
            words = tweet.split()
            long_word = max(words, key=lambda s: len(s))
            #print(f"the tweet number {i} has longest word {long_word}")
            k[i] = long_word
            i+=1
        return k
    def num_follow(self):
        print (f" {self.handle} has {self.tweets[0].user.followers_count} followers")

# kaushik = Twitter_user('Kaushik0106')
# print(kaushik.avg_len())
# print(kaushik.longest_word())
# kaushik.num_follow()





## Brain dump###

# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")

# define a handle to inspect for quicker reference
# handle = 'codingnomads' # for example purposes; prop any handle you want!
# tweets = api.user_timeline(screen_name="Kaushik0106")
# for tweet in tweets:
#     print(f"{tweet.user.name} and {tweet.user.followers_count}")
#print(tweets)
# # write tweet data to a JSON file
# tweet_list = []
# tweet_words = []
# tweet_character = []
# for tweet in tweets:
# #     pprint(tweet._json['user']['followers_count'])  # uncomment to see the tweet data
#     tweet_list.append(tweet.text)
# #The average length of tweets (in characters)
# for tweet2 in tweet_list:
#   words = tweet2.split()
#   tweet_words.append(len(words))
#   for word in words:
#       tweet_character.append(len(word))
#
# avg_char = sum(tweet_character) / len(tweet_words)
# print(f"The average number of character per tweet is {avg_char}")
#
# #The longest word in a single tweet
# i = 1
# for tweet in tweet_list:
#     words = tweet.split()
#     long_word = max(words, key=lambda s: (len(s), s))
#     print(f"the tweet number {i} has longest word {long_word}")
#     i+=1
# #print(tweet_list)
#
# #The average number of followers this user has
# print(f"{tweets[0].user.name} has {tweets[0].user.followers_count} followers")
#
# with open('data.json', 'w') as f:
#     json.dump(tweet_list, f)
