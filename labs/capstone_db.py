import os
import sqlalchemy
from pprint import pprint
import tweepy
import json
from pprint import pprint
from collections import Counter
from datetime import datetime
import capstone_tweepy
from datetime import datetime

#fetch the secrets from our virtual environment variables
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

engine = sqlalchemy.create_engine('mysql+pymysql://root:'+os.environ['KEY_ID']+'@localhost/twitter_database')
connection = engine.connect()
metadata = sqlalchemy.MetaData()


twitter_database = sqlalchemy.Table('twitter_data', metadata,
                            sqlalchemy.Column('created_at', sqlalchemy.DateTime(40)),
                            sqlalchemy.Column('id', sqlalchemy.BigInteger()),
                            sqlalchemy.Column('id_str', sqlalchemy.String(100)),
                            sqlalchemy.Column('text', sqlalchemy.String(200)),
                            sqlalchemy.Column('user_name', sqlalchemy.String(20)),
                            sqlalchemy.Column('followers_count', sqlalchemy.Integer()),
                            sqlalchemy.Column('tweet_count', sqlalchemy.Integer())
                    )
twitter_data_results = sqlalchemy.Table('twitter_results', metadata,
                            sqlalchemy.Column('keyword_search', sqlalchemy.String(255)),
                            sqlalchemy.Column('avg_num_followers', sqlalchemy.Float()),
                            sqlalchemy.Column('avg_tweet_length_word', sqlalchemy.Float()),
                            sqlalchemy.Column('avg_tweet_length_char', sqlalchemy.Float()),
                            sqlalchemy.Column('tweet_with_hash', sqlalchemy.Float()),
                            sqlalchemy.Column('tweet_with_mention', sqlalchemy.Float()),
                            sqlalchemy.Column('common_words', sqlalchemy.JSON(300)),
                            sqlalchemy.Column('common_symbol', sqlalchemy.JSON(300)),
                            sqlalchemy.Column('tweet_with_punctuation', sqlalchemy.Float()),
                            sqlalchemy.Column('longest_word', sqlalchemy.JSON(200)),
                            sqlalchemy.Column('shortest_word', sqlalchemy.JSON(300)),
                            sqlalchemy.Column('user_max_tweets', sqlalchemy.String(255)),
                            sqlalchemy.Column('avg_tweet_count', sqlalchemy.Float()),
                            sqlalchemy.Column('tweet_hour', sqlalchemy.JSON())
                        )
metadata.create_all(engine)
newTable1 = sqlalchemy.Table('twitter_data', metadata, autoload=True, autoload_with=engine)
for tweet in tweets:
    query_data = sqlalchemy.insert(newTable1).values(created_at=tweet.created_at, id=tweet.id, id_str=tweet.id_str, text=tweet.text, user_name=tweet.user.screen_name, followers_count=tweet.user.followers_count, tweet_count=tweet.user.statuses_count)
    result_proxy = connection.execute(query_data)



query1 = sqlalchemy.select([newTable1.c.followers_count])
result_proxy1 = connection.execute(query1)
result_set1 = result_proxy1.fetchall()
response1 = [value for (value,) in result_set1]
query2 = sqlalchemy.select([newTable1.c.text])
result_proxy2 = connection.execute(query2)
result_set2 =  result_proxy2.fetchall()
response2 = [value for (value,) in result_set2]
query3 = sqlalchemy.select([newTable1.c.user_name])
result_proxy3 = connection.execute(query3)
result_set3 =  result_proxy3.fetchall()
response3 = [value for (value,) in result_set3]
query4 = sqlalchemy.select([newTable1.c.tweet_count])
result_proxy4 = connection.execute(query4)
result_set4 =  result_proxy4.fetchall()
response4 = [value for (value,) in result_set4]
response5 = dict(zip(response3, response4))
query6 = sqlalchemy.select([newTable1.c.created_at])
result_proxy6 = connection.execute(query6)
result_set6 =  result_proxy6.fetchall()
response6 = [value for (value,) in result_set6]
response_hour = [i.strftime('%H') for i in response6]



def avg_num_followers(response):
    return sum(response)/len(response)
num_follow_db = avg_num_followers(response1)

len_words_db = capstone_tweepy.avg_len_words(response2)
len_char_db = capstone_tweepy.avg_len_char(response2)
with_h_db = capstone_tweepy.tweet_with_hash(response2)
with_m_db = capstone_tweepy.tweet_with_mention(response2)
comm_words_db = capstone_tweepy.tweet_common_words(response2)
comm_sym_db = capstone_tweepy.tweet_common_symbols(response2)
with_p_db = capstone_tweepy.tweet_with_punctuation(response2)
long_word_db = capstone_tweepy.tweet_longest_word(response2)
short_word_db = capstone_tweepy.tweet_shortest_word(response2)

def tweet_user_max(response):
    max_tweet_user = max(response, key=response.get)
    return max_tweet_user

status_count_db = tweet_user_max(response5)

def avg_tweet_count(tweet_count):
    return sum(tweet_count)/len(tweet_count)

avg_t_db = avg_tweet_count(response4)


def tweet_hour_max(create_time):
    counts = Counter(create_time).most_common(1)
    count = dict(counts)
    return count

max_h_db = tweet_hour_max(response_hour)

newTable2 = sqlalchemy.Table('twitter_results', metadata, autoload=True, autoload_with=engine)
#query = sqlalchemy.insert(newTable2).values(avg_num_followers=num_follow_db, avg_tweet_length_word=len_words_db)
query = sqlalchemy.insert(newTable2).values(keyword_search='python', avg_num_followers=num_follow_db, avg_tweet_length_word=len_words_db, avg_tweet_length_char=len_char_db, tweet_with_hash=with_h_db, tweet_with_mention=with_m_db, common_words=comm_words_db, common_symbol=comm_sym_db, tweet_with_punctuation=with_p_db, longest_word=long_word_db, shortest_word=short_word_db, user_max_tweets=status_count_db, avg_tweet_count=avg_t_db, tweet_hour=max_h_db)
#avg_tweet_length_char=len_char_db, tweet_with_hash=with_h_db, tweet_with_mention=with_m_db, 10_common_words=comm_words_db, 10_common_symbol=comm_sym_db, tweet_with_punctuation=with_p_db, longest_word=long_word_db, shortest_word=short_word_db, user_max_tweets=status_count_db, avg_tweet_count=avg_t_db, tweet_hour=max_h_db)

result_proxy = connection.execute(query)
