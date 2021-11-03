__author__ = 'Abduljaleel'

import json
import tweepy as tweepy
from twitter import *
import pprint
import Utility

# Load Twitter API secrets from an external JSON file
secrets = json.loads(open('secrets.json').read())
api_key = secrets['api_key']
api_secret_key = secrets['api_secret_key']
access_token = secrets['access_token']
access_token_secret = secrets['access_token_secret']


# Connect to Twitter API using the secrets
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api_tweepy = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify="Please Waite, The rate limit is exceeded.")

api = Twitter(auth=OAuth(access_token, access_token_secret, api_key, secrets))

q0 = "java script"
q1 = "((JavaScript) OR (Python) OR (HTML) OR (C programming language) OR (C++) OR (Java) OR (R programming language) OR (R language) OR (C#) OR (C Sharp) OR (Go programming language) OR (Swift programming language))"
q2 = "(ROS OR robotics deep learning OR reinforcement learning OR machine learning OR reinforcement learning OR tensorflow OR pytorch OR computer vision OR artificial intelligence OR robot OR deep learning OR robotics)"
q3 = "((programming language) OR (programming) OR (coding) OR (developer) OR (developing))"
query = q0
print query
date_since = "2021-09-14"
date_until = "2021-09-15"
tweets_search_result = tweepy.Cursor(api_tweepy.search, q=query, lang="en", result_type="mixed", tweet_mode = "extended").items(100)

for results in tweets_search_result:
    tweet = results._json
    text = tweet['full_text']
    if tweet.get('entities').get('media'):
        tweet_media_exist = True                                    # True if the tweet includes media
    else:
        tweet_media_exist = False                                   # False if the tweet doesn't includes media
    text = tweet['full_text']                                       # Text

    if ('RT' not in text) and ('http' not in text):
        # pprint.pprint (tweet)

        id = tweet['id']                                                # tweet id
        created_at = tweet['created_at']                                # the creation date
        tweet_url = 'https://twitter.com/twitter/statuses/'+str(id)     # tweet url
        retweeted = tweet['retweeted']                                  # Retweeted?
        retweet_count = tweet['retweet_count']                          # number of retweets
        tweet_likes = tweet['favorite_count']                           # number of the likes
        hashtags = tweet['entities']['hashtags']                        # a list of the hash-tags
        user_name = tweet['user']['screen_name']                        # user's name
        user_followers_count = tweet['user']['followers_count']         # user's followers count
        user_friends_count = tweet['user']['friends_count']             # user's friends count
        user_id = tweet['user']['id']                                   # user's id
        user_created_at = tweet['user']['created_at']                   # user account's age
        user_listed_count = tweet['user']['listed_count']               # The number of public lists that this user is a member of
        user_statuses_count = tweet['user']['statuses_count']           # The number of Tweets (including retweets) issued by the user.
        user_url = tweet['user']['url']                                 # A URL provided by the user in association with their profile.
        is_user_verified = tweet['user']['verified']                    # When true, indicates that the user has a verified account.
        user_description = tweet['user']['description']

        data_object = {
            "created_at" : created_at,
            "tweet_url": tweet_url,
            "text": text,
            "retweeted": retweeted,
            "retweet_count" : retweet_count,
            "tweet_likes": tweet_likes,
            "hashtags": hashtags,
            "user_name": user_name,
            "user_followers_count": user_followers_count,
            "user_friends_count": user_friends_count,
            "user_id": user_id,
            "user_created_at": user_created_at,
            "tweet_media_exist": tweet_media_exist,
            "user_listed_count": user_listed_count,
            "user_statuses_count": user_statuses_count,
            "user_url": user_url,
            "is_user_verified": is_user_verified,
            "user_description": user_description
        }

        pprint.pprint(data_object)


        # tw = tweepy.Cursor(api_tweepy.search,q='to:'+name, result_type="recent").items(1000)
        # for tt in tw:
        #     if hasattr(tt, 'in_reply_to_status_id_str'):
        #         print tt.in_reply_to_status_id_str
        #         print tweet_id
        #         print '***'
        #         if (str(tt.in_reply_to_status_id_str) == str(tweet_id)):
        #             print ('found reply')
        print "------"*20


# How to build a query
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
# (JavaScript OR Python OR HTML OR C programming language OR C++ OR Java OR R programming language OR R language OR C# OR C Sharp OR Go programming language OR Swift)
# (ROS OR robotics deep learning OR reinforcement learning OR machine learning OR reinforcement learning OR tensorflow OR pytorch OR computer vision OR artificial intelligence OR robot OR deep learning OR robotics)
# (programming language OR programming OR code OR coding OR developer OR developing OR development OR design OR designing OR implementation OR implementing)


#  find the search words (including language, ROS)
# no duplicate tweets
# filter out the add tweets
# save to mongo db
# find reply counts
# store repliers info
# update in mongo db

# Show Twitter API limits
limit = int(api_tweepy.last_response.headers['x-rate-limit-limit'])
remaining = int(api_tweepy.last_response.headers['x-rate-limit-remaining'])
seconds_to_reset = int(api_tweepy.last_response.headers['x-rate-limit-reset'])
Utility.show_limits(limit,remaining,seconds_to_reset)

