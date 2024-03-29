import os
import tweepy
import json
from pprint import pprint
from collections import Counter
from datetime import datetime






def avg_num_followers(tweets):
    """
    This counts the average number of followers  twitter users has who typed 'python' keyword
    Args:
        list of tweets with the tweet metadata
    Returns:
        float: average number of followers
    """
    follower_list = []
    for i in tweets:
        follower_list.append(i.user.followers_count)
    return sum(follower_list) / len(follower_list)


def tweet_text(tweets):
    """
    This gives a list of tweets text
    Args:
        list of tweets with the tweet metadata
    Returns:
        list: text from each tweet
    """
    tweet_text_list = []
    for tweet in tweets:
        tweet_text_list.append(tweet.text)
    return tweet_text_list

def avg_len_words(tweet_list):
    """
    This gives average length of the words in tweets
    Args:
        list: text from each tweet
    Returns:
        float: average length
    """
    tweet_words = []
    for text in tweet_list:
        words = text.split()
        tweet_words.append(len(words))
    return sum(tweet_words) / len(tweet_words)

def avg_len_char(tweet_list):
    """
    This gives average length of the characters in tweets
    Args:
        list: text from each tweet
    Returns:
        float: average length
    """
    tweet_words = []
    tweet_character = []
    for tweet in tweet_list:
      words = tweet.split()
      tweet_words.append(len(words))
      for word in words:
          tweet_character.append(len(word))
    return sum(tweet_character) / len(tweet_words)

def tweet_with_hash(tweet_list):
    """
    This gives % of tweets with hash(#) in it
    Args:
        list: text from each tweet
    Returns:
        float: percentage
    """
    tweet_hash = 0
    for tweet in tweet_list:
        if '#' in tweet:
            tweet_hash+=1
    return (tweet_hash/len(tweet_list))*100

def tweet_with_mention(tweet_list):
    """
    This gives % of tweets with mentioning(@) other user
    Args:
        list: text from each tweet
    Returns:
        float: percentage
    """
    tweet_men = 0
    for tweet in tweet_list:
        if '@' in tweet:
            tweet_men+=1
    return (tweet_men/len(tweet_list))*100



def tweet_common_words(tweet_list):
    """
    This gives 10 most common words in the tweets
    Args:
        list: text from each tweet
    Returns:
        dictionary: {word:occurance_count}
    """
    words_list = []
    for tweet in tweet_list:
        words = tweet.split()
        for word in words:
            words_list.append(word.lower())
    counts = Counter(words_list).most_common(10)
    most_common = dict(counts)
    return most_common


def tweet_common_symbols(tweet_list):
    """
    This gives 10 most common symbols in the tweets
    Args:
        list: text from each tweet
    Returns:
        dictionary: {symbol: occurance_count}
    """
    sym_list = []
    for tweet in tweet_list:
        words = tweet.split()
        for word in words:
            for char in word:
                if char.isalpha() == False and char.isdigit() == False:
                    sym_list.append(char)
    counts = Counter(sym_list).most_common(10)
    most_common = dict(counts)
    return most_common


def tweet_with_punctuation(tweet_list):
    """
    This gives % tweets with punctuation
    Args:
        list: text from each tweet
    Returns:
        float: percentage
    """
    tweet_punc = 0
    punctuations = [',', ';', ':', '.', '!', '?', "'", '"', '_', '-', '/', '(', ')', '[', ']', '...', '*']
    for tweet in tweet_list:
        res = any(ele in tweet for ele in punctuations)
        if res == True:
            tweet_punc+=1
    return (tweet_punc/len(tweet_list))*100

def tweet_longest_word(tweet_list):
    """
    This gives longest word in each tweet
    Args:
        list: text from each tweet
    Returns:
        dictionary: {tweet_count: word}
    """
    i = 1
    k = {}
    for tweet in tweet_list:
        words = tweet.split()
        words_list = []
        for word in words:
            for char in word:
                if char.isalpha() == True:
                    words_list.append(word)
        long_word = max(words, key=lambda s: len(s))
        #print(f"the tweet number {i} has longest word {long_word}")
        k[i] = long_word
        i+=1
    return k

def tweet_shortest_word(tweet_list):
    """
    This gives shortest word in each tweet
    Args:
        list: text from each tweet
    Returns:
        dictionary: {tweet_count: shortest}
    """
    i = 1
    k = {}
    for tweet in tweet_list:
        words = tweet.split()
        words_list = []
        for word in words:
            for char in word:
                if char.isalpha() == True:
                    words_list.append(word)
        short_word = min(words_list, key=lambda s: len(s))
        k[i] = short_word
        i+=1
    return k

def tweet_user_max(tweets):
    """
    This gives user with maximum tweets
    Args:
        list: list of tweets with the tweet metadata
    Returns:
        string: screen_name
    """
    user_list = {}
    for tweet in tweets:
        user = tweet.user.screen_name
        tweet_count = tweet.user.statuses_count
        user_list[user] = tweet_count
    max_tweet_user = max(user_list, key=user_list.get)
    return max_tweet_user

def avg_tweet_count(tweets):
    """
    This gives average number of tweets by users
    Args:
        list: list of tweets with the tweet metadata
    Returns:
        float: number
    """
    tweet_count = []
    for tweet in tweets:
        tweet_count.append(tweet.user.statuses_count)
    return sum(tweet_count)/len(tweet_count)


def tweet_hour_max(tweets):
    """
    This gives the hour when users tweeted the most
    Args:
        list: list of tweets with the tweet metadata
    Returns:
        dictionary: {hour:count}
    """
    create_time = []
    for tweet in tweets:
        create_time.append(tweet.created_at.strftime('%H'))
    counts = Counter(create_time).most_common(1)
    count = dict(counts)
    return count



def run():
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
    tweets = [item for item in tweepy.Cursor(api.search,
             q="python",
             lang="en",
             since=2019-8-16).items(20)]
    tweet_list = tweet_text(tweets)

    print(f"Average number of followers of one user is {avg_num_followers(tweets)}")
    print(f"Average length of words of each tweet is {avg_len_words(tweet_list)}")
    print(f"Average length of character of each tweet is {avg_len_char(tweet_list)}")
    print(f"{tweet_with_hash(tweet_list)} percentage of tweets with hash")
    print(f"{tweet_with_mention(tweet_list)}percentage of tweets with mention")
    print(f"10 Most common words are: \n {tweet_common_words(tweet_list)}")
    print(f"10 Most common symbols are: \n{tweet_common_symbols(tweet_list)}")
    print(f"{tweet_with_punctuation(tweet_list)} percentage of tweets with punctuation")
    print(f"Longest word in each tweet is {tweet_longest_word(tweet_list)}")
    print(f"Shortest word in each tweet is{tweet_shortest_word(tweet_list)}")
    print(f"User with the highest number of tweets is {tweet_user_max(tweets)}")
    print(f"Average number of tweets from users are {avg_tweet_count(tweets)}")
    print(f"Most common hour of tweet is {tweet_hour_max(tweets)}")







if __name__ == "__main__":
    run()



# import os
# import sqlalchemy
# from pprint import pprint
# engine = sqlalchemy.create_engine('mysql+pymysql://root:'+os.environ['KEY_ID']+'@localhost/sakila')
# connection = engine.connect()
# metadata = sqlalchemy.MetaData()

# tweet_list = []
# for tweet in tweets:
#     # pprint(tweet._json)  # uncomment to see the tweet data
#     tweet_list.append(tweet._json)
#
# with open('data.json', 'w') as f:
#     json.dump(tweet_list, f)
