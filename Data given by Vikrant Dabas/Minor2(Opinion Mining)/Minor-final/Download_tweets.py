__author__ = 'shubham'

import sys
from twython import Twython
consumer_key = "RGVO3CTujE60TW5IQy1JwmyxF"
consumer_secret = "ziWzApZCAqlwOt3xK3L0B02VjEsDFZg4Fniy76TsTLKgtnjqlG"
access_key = "1587880604-1tjWpdETzVE4fPALCGeNs6O2oHi4y8ShwIsDQSl"
access_secret = "wJHBahm2y3KnTXuuj2JX18GAolaHVMnLKZ7Ygc0LxnQMH"

APP_KEY = consumer_key
APP_SECRET = consumer_secret
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
alltweets = []

#make initial request for most recent tweets (200 is the maximum allowed count)

user_timeline = twitter.get_user_timeline(screen_name=sys.argv[1],count=200,include_rts=1)
alltweets.extend(user_timeline)
oldest = alltweets[-1]['id'] - 1

#keep grabbing tweets until there are no tweets left to grab
while len(user_timeline) > 0:
	user_timeline = twitter.get_user_timeline(screen_name=sys.argv[1],count=200,include_rts=1,max_id=oldest)
	alltweets.extend(user_timeline)
	oldest = alltweets[-1]['id']-1

global count
count=0
f=open(sys.argv[1]+'tweets.txt','a')

for tweet in alltweets:
    count+=1
    print(tweet['text'])
    f.write(tweet['text'])
    f.write("\n")


print(count)


#twitter = Twython()
# First, let's grab a user's timeline. Use the
# 'screen_name' parameter with a Twitter user name.
#user_timeline = twitter.get_user_timeline()