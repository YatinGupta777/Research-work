import tweepy
import csv
import json

# load Twitter API credentials
####input your credentials here
consumer_key = "RGVO3CTujE60TW5IQy1JwmyxF"
consumer_secret = "ziWzApZCAqlwOt3xK3L0B02VjEsDFZg4Fniy76TsTLKgtnjqlG"
access_token = "1587880604-1tjWpdETzVE4fPALCGeNs6O2oHi4y8ShwIsDQSl"
access_token_secret = "wJHBahm2y3KnTXuuj2JX18GAolaHVMnLKZ7Ygc0LxnQMH"


def get_all_tweets(screen_name):

    # Twitter allows access to only 3240 tweets via this method
    
    # Authorization and initialization
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    # initialization of a list to hold all Tweets
    
    all_the_tweets = []
    
    # We will get the tweets with multiple requests of 200 tweets each
    
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    
    # saving the most recent tweets
    
    all_the_tweets.extend(new_tweets)
    
    # save id of 1 less than the oldest tweet
    
    oldest_tweet = all_the_tweets[-1].id - 1
    
    # grabbing tweets till none are left
    
    while len(new_tweets) > 0:
    # The max_id param will be used subsequently to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name,
                                       count=200, max_id=oldest_tweet)
    
    # save most recent tweets
    
    all_the_tweets.extend(new_tweets)
    
    # id is updated to oldest tweet - 1 to keep track
    
    oldest_tweet = all_the_tweets[-1].id - 1
    print ('...%s tweets have been downloaded so far' % len(all_the_tweets))
    
    # transforming the tweets into a 2D array that will be used to populate the csv
    
#    outtweets = [[tweet.id_str, tweet.created_at,
#    tweet.text.encode('utf-8')] for tweet in all_the_tweets]

    return all_the_tweets
    # writing to the csv file
    
# =============================================================================
#     with open(screen_name + '_tweets.csv', 'w', encoding='utf8') as f:
#     writer = csv.writer(f)
#     writer.writerow(['id', 'created_at', 'text'])
#     writer.writerows(outtweets)
# =============================================================================
    
if __name__ == '__main__':
 
    # Enter the twitter handle of the person concerned 
    tweets = []
    tweets = get_all_tweets("elonmusk")
    print(tweets)
    