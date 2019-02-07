#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import csv
import json

# Twitter API credentials

consumer_key = "RGVO3CTujE60TW5IQy1JwmyxF"
consumer_secret = "ziWzApZCAqlwOt3xK3L0B02VjEsDFZg4Fniy76TsTLKgtnjqlG"
access_token = "1587880604-1tjWpdETzVE4fPALCGeNs6O2oHi4y8ShwIsDQSl"
access_token_secret = "wJHBahm2y3KnTXuuj2JX18GAolaHVMnLKZ7Ygc0LxnQMH"

# Create the api endpoint

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

# Mention the maximum number of tweets that you want to be extracted.

maximum_number_of_tweets_to_be_extracted = 2000
# Mention the hashtag that you want to look out for

hashtag = "#Google"
tweets = []
for tweet in tweepy.Cursor(api.search, q=hashtag,rpp=100).items(maximum_number_of_tweets_to_be_extracted):
    tweets.append((str(tweet.text.encode('utf-8')) + '\n'))


print ('Extracted ' + str(len(tweets)) \
    + ' tweets with hashtag ' + hashtag)

# =============================================================================
# 
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     api = tweepy.API(auth,wait_on_rate_limit=True)
#     list_tweets = []
#     for tweet in tweepy.Cursor(api.search,q=hashtag,count=number_of_tweets,
#        lang="en",
#        since="2017-04-03").items():
#        list_tweets.append(tweet.text) 
#        
#     
#     new_file = hashtag + ".txt"
#     handle = open(new_file, "w+")
#     for i in list_tweets:
#         handle.write(i)  
#         
#     return list_tweets
# =============================================================================
