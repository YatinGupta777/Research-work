
import tweepy
from time import sleep
import csv
import nltk
#nltk.download()
from tkinter import*
import tkinter as ttk
from twitter import *
import twitter

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler


consumer_key = "RGVO3CTujE60TW5IQy1JwmyxF"
consumer_secret = "ziWzApZCAqlwOt3xK3L0B02VjEsDFZg4Fniy76TsTLKgtnjqlG"
access_key = "1587880604-1tjWpdETzVE4fPALCGeNs6O2oHi4y8ShwIsDQSl"
access_secret = "wJHBahm2y3KnTXuuj2JX18GAolaHVMnLKZ7Ygc0LxnQMH"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
t = Twitter(
    auth=OAuth(access_key, access_secret, consumer_key, consumer_secret))

#Function to download tweets corresponding to a hash tag.

def get_all_hash(hashtag):

    #hashtag = name
    api = tweepy.API(auth)
    print("FYI , the following trending topics are available")
    trends1 = api.trends_place(1)
    trends = set([trend['name'] for trend in trends1[0]['trends']])
    print(trends)
    print("Tweets downloading has started !!")

    '''
    cricTweet = tweepy.Cursor(api.search, q=hashtag).items(179)
    for tweet in cricTweet:
    print (tweet.text)
    with open('hashtag_tweets','w') as f:
    	for tweet in cricTweet:
    	f.write(tweet.text)
    '''

    searchQuery = '#someHashtag'  # this is what we're searching for
    maxTweets = 5000 # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits
    fName = 'tweets.txt' # We'll store the tweets in a text file.


    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    with open(fName, 'w') as f:
        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = api.search(q=hashtag, count=tweetsPerQry)
                    else:
                        new_tweets = api.search(q=hashtag, count=tweetsPerQry, since_id=sinceId)
                else:
                        if (not sinceId):
                            new_tweets = api.search(q=hashtag, count=tweetsPerQry, max_id=str(max_id - 1))
                        else:
                            new_tweets = api.search(q=hashtag, count=tweetsPerQry, max_id=str(max_id - 1), since_id=sinceId)
                        if not new_tweets:
                            print("No more tweets found")
                            break
                list_tweets = []
                for tweet in new_tweets:
                    list_tweets.append(tweet.text)
                    tweetCount += len(new_tweets)
                    print("Downloaded {0} tweets".format(tweetCount))
                    max_id = new_tweets[-1].id
                   # except tweepy.TweepError as e:
                                # Just exit if any error
                    #        print("some error : " + str(e))
                     #       break
                    z=open(hashtag+'.txt','w')
                for tweet in list_tweets:
                    tweet=tweet.encode('ascii','ignore')
                    z.write(tweet.decode())
                    z.write("\n")
                z.close()
            except tweepy.TweepError as e:
                # Just exit if any error
                    print("some error : " + str(e))
                    break

    return list_tweets

#print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
#Function to download tweets corresponding to an username.
def get_all_tweets(username):

    alltweets = []
    user_timeline = t.statuses.user_timeline(screen_name=username,count=200,include_rts=1)
    alltweets.extend(user_timeline)
    oldest = alltweets[-1]['id'] - 1

        #keep grabbing tweets until there are no tweets left to grab
    while len(user_timeline) > 0:
        user_timeline = t.statuses.user_timeline(screen_name=username,count=200,include_rts=1,max_id=oldest)
        alltweets.extend(user_timeline)
        oldest = alltweets[-1]['id']

    tweets = []
    for tweet in alltweets:
        tweets.append(tweet['text'])
    return tweets

#Data cleaning Functions:
def isEnglish(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

    #The following function removes the part of the string that contains the substring eg. if
    #substring = 'http' , then http://www.google.com is removed, that means, remove until a space is found
def rem_substring(tweets,substring):
    m=0;
            #print(len(tweets))
    for i in tweets:
        while i.find(substring)!=-1:
            k=i.find(substring)
            d=i.find(' ',k,len(i))
            if d!=-1:               #substring is present somwhere in the middle(not the end of the string)
                i=i[:k]+i[d:]
            else:                   #special case when the substring is present at the end, we needn't append the
                i=i[:k]             #substring after the junk string to our result
        tweets[m]=i #store the result in tweets "list"
        m+= 1
    return tweets

#The following function removes the non English tweets .Makes use of the above written isEnglish Function
def removeNonEnglish(tweets):
    result=[]
    for i in tweets:
        if isEnglish(i):
            result.append(i)
    return result


#the following function converts all the text to the lower case
def lower_case(tweets):
    result=[]
    for i in tweets:
        result.append(i.lower())
    return result

def rem_punctuation(tweets,punct):
    #print(len(tweets))
    m=0
    for i in tweets:
        i=i.replace(punct,'')
        tweets[m]=i
        m=m+1
    return tweets

def score(name):
    filename = 'a.csv'
    count_adj=0
    count=0
    ans=[]
    list_words = []
    ans.append(0)
    ans.append(0)
    ans.append(0)
    ans.append(0)
    ans.append(0)
    special_word=None
    special_score=0 ###CHANGED FROM NONE

        #r=open(sys.argv[1],'r')
    for line in name:
        line=line.lower()
        line=line.replace("."," ")
        line=line.split(" ")
        list_words=line
    #    print(list_words[0])

    for word in list_words:
        with open(filename,encoding="ISO-8859-1",newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                #print(row)
                my_list = row
                word = word.lower()
                if (word == my_list[0] and len(word)>=1):
                    ans_list=[]
                    count_adj+=1
                    #print(count)
                    ans_list.append(word)
                    ans_list.append(my_list[1])
                    ans_list.append(my_list[3])
                    ans_list.append(my_list[5])
                    ans_list.append(my_list[7])
                    ans_list.append(my_list[9])


        #FIX THISSS

                if special_word is None:
                    ans[0]+=float(my_list[1])
                    ans[1]+=float(my_list[3])
                    ans[2]+=float(my_list[5])
                    ans[3]+=float(my_list[7])
                    ans[4]+=float(my_list[9])
                else:
                    print(special_word,word)
                    print(special_score)
                if special_score>=0:
                    ans[0]+=float(my_list[1])*max(0.5,float(special_score))
                    ans[1]+=float(my_list[3])*max(0.5,float(special_score))
                    ans[2]+=float(my_list[5])*max(0.5,float(special_score))
                    ans[3]+=float(my_list[7])*max(0.5,float(special_score))
                    ans[4]+=float(my_list[9])*max(0.5,float(special_score))
                else:
                    ans[0]+=5-float(my_list[1])
                    ans[1]+=5-float(my_list[3])
                    ans[2]+=5-float(my_list[5])
                    ans[3]+=5-float(my_list[7])
                    ans[4]+=5-float(my_list[9])
                    special_word=None
                            #final_list.append(ans_list)
                            #print(ans_list)
        break

    #FILENAME CHANGED FOR DEBUGGING ORIGINAL == 'adverb.csv'

        with open(filename,encoding="ISO-8859-1",newline='') as a:
            reader=csv.reader(a)
            for row in reader:
                list_adverb=row
                            #print(list_adverb)
                word=word.lower()
                if (word==list_adverb[0]):
                    count+=1
                    ans_list=[]
                    ans_list.append(word)
                    ans_list.append(list_adverb[1])
                    ans_list.append(list_adverb[1])
                    ans_list.append(list_adverb[1])
                    ans_list.append(list_adverb[1])
                    ans_list.append(list_adverb[1])
                                #ans[0]+=float(list_adverb[1])
                                #ans[1]+=float(list_adverb[1])
                                #ans[2]+=float(list_adverb[1])
                                #ans[3]+=float(list_adverb[1])
                                #ans[4]+=float(list_adverb[1])

                #FIX THISS BELOWW

                if special_word is None:
                    special_word=word
                    special_score=float(list_adverb[1])
                else:
                    special_word=word
                    special_score=float(special_score)*float(list_adverb[1])

                                        #print(ans_list)
                break


        #FILENAME CHANGED FOR DEBUGGING ORIGINAL == 'verb.csv'

        with open(filename,encoding="ISO-8859-1",newline='') as v:
            reader=csv.reader(v)
            for row in reader:
                list_verb=row
                word=word.lower()
                            #print(list_adverb)
                if (word==list_verb[0]):
                    count+=1

                #FIX THIS BELOW

                ans_list=[]
                ans_list.append(word)
                ans_list.append(list_verb[1])
                ans_list.append(list_verb[1])
                ans_list.append(list_verb[1])
                ans_list.append(list_verb[1])
                ans_list.append(list_verb[1])

                #FIX THIS BELOW


                if special_word is None:
                    special_word=word
                    special_score=float(list_verb[1])
                else:
                    special_word=word
                    special_score=float(special_score)*float(list_verb[1])

                                        #print(ans_list)
                break


            #print(count)
            #print(ans)
        for i in range(0,5):
                #ans[i]=ans[i]/((5*count_adj)+count)
            if count_adj != 0:
                ans[i]=ans[i]/(5*count_adj)
    print(ans)
    return ans


#Scoring Module 2

def score2(name):
        # count_adj=0
    filename = 'data_emotions_words_list.csv'
    count = 0
    ans = []
    ans.append(0)
    ans.append(0)
    ans.append(0)
    ans.append(0)
    ans.append(0)
        # r=open(name,'r')
    count_adj = 0
        # count_verb=0
    adj_ans = []
    adj_ans.append(0)
    adj_ans.append(0)
    adj_ans.append(0)
    adj_ans.append(0)
    adj_ans.append(0)
    adv_ans = []
    adv_ans.append(0)
    adv_ans.append(0)
    adv_ans.append(0)
    adv_ans.append(0)
    adv_ans.append(0)

     # r=open(sys.argv[1],'r')
    for line in name:
        line = line.lower()
        line = line.replace(".", " ")
        line = line.split(" ")
        list_words = line
            #    print(list_words[0])
        for word in list_words:
            with open("data_emotions_words_list.csv", encoding="ISO-8859-1", newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    my_list = row
                    word = word.lower()
                    if (word == my_list[0] and len(word) >= 1):
                        ans_list = []
                        count_adj += 1
                            # print(count)
                        ans_list.append(word)
                        ans_list.append(my_list[1])
                        ans_list.append(my_list[3])
                        ans_list.append(my_list[5])
                        ans_list.append(my_list[7])
                        ans_list.append(my_list[9])
                        adj_ans[0] += float(my_list[1])
                        adj_ans[1] += float(my_list[3])
                        adj_ans[2] += float(my_list[5])
                        adj_ans[3] += float(my_list[7])
                        adj_ans[4] += float(my_list[9])

                        # final_list.append(ans_list)
                        # print(ans_list)
                        break
#FILENAME CHANGED ORIGINAL == 'adverb.csv'

    with open(filename, encoding="ISO-8859-1", newline='') as a:
        reader = csv.reader(a)
        for row in reader:
            list_adverb = row
                # print(list_adverb)
            word = word.lower()
            if (word == list_adverb[0]):
                count += 1
                ans_list = []
                ans_list.append(word)
                ans_list.append(list_adverb[1])
                ans_list.append(list_adverb[1])
                ans_list.append(list_adverb[1])
                ans_list.append(list_adverb[1])
                ans_list.append(list_adverb[1])
                adv_ans[0] += float(list_adverb[1])
                adv_ans[1] += float(list_adverb[1])
                adv_ans[2] += float(list_adverb[1])
                adv_ans[3] += float(list_adverb[1])
                adv_ans[4] += float(list_adverb[1])

                    # print(ans_list)
                break
#FILENAME CHANGED ORIGINAL == 'verb.csv'
    with open(filename, encoding="ISO-8859-1", newline='') as v:
        reader = csv.reader(v)
        for row in reader:
            list_verb = row

            word = word.lower()
                 # print(list_adverb)
            if (word == list_verb[0]):
                count += 1
                ans_list = []
                ans_list.append(word)
                ans_list.append(list_verb[1])
                ans_list.append(list_verb[1])
                ans_list.append(list_verb[1])
                ans_list.append(list_verb[1])
                ans_list.append(list_verb[1])
                adv_ans[0] += float(list_verb[1])
                adv_ans[1] += float(list_verb[1])
                adv_ans[2] += float(list_verb[1])
                adv_ans[3] += float(list_verb[1])
                adv_ans[4] += float(list_verb[1])

                    # print(ans_list)
                break

                    ##########ARBITARY VALUE
            count_adj = 3
                    #############

            if adj_ans[0] / count_adj > 3:
                ans[0] = ((adj_ans[0] / 3.725) + adv_ans[0]) / (count + count_adj)
            else:
                ans[0] = ((adj_ans[0] / 3.725) - adv_ans[0]) / (count + count_adj)

            if adj_ans[2] / count_adj > 3:
                ans[2] = ((adj_ans[2] / 3.4875) + adv_ans[2]) / (count + count_adj)
            else:
                ans[2] = ((adj_ans[2] / 3.4875) - adv_ans[2]) / (count + count_adj)

            if adj_ans[4] / count_adj > 3:
                ans[4] = ((adj_ans[4] / 2.665) + adv_ans[4]) / (count + count_adj)
            else:
                ans[4] = ((adj_ans[4] / 2.665) - adv_ans[4]) / (count + count_adj)

            if adj_ans[1] / count_adj > 3:
                ans[1] = ((adj_ans[1] / 2.5) + adv_ans[1]) / (count + count_adj)
            else:
                ans[1] = ((adj_ans[1] / 2.5) - adv_ans[1]) / (count + count_adj)

            if adj_ans[3] / count_adj > 3:
                ans[3] = ((adj_ans[3] / 2.5) + adv_ans[3]) / (count + count_adj)
            else:
                ans[3] = ((adj_ans[3] / 2.5) - adv_ans[3]) / (count + count_adj)

    print(ans)
    return ans

    #POS Tagger Function used to identify the adjectives, verbs, adverbs.
def POS_tagger(tweets, username):
    x = []
        # for each line in tweets list
    for line in tweets:
        tokenized = nltk.sent_tokenize(line)
        t = ""
            # for each sentence in the line
        for sent in tokenized:
                # tokenize this sentence
            text = nltk.word_tokenize(sent)
            k = nltk.pos_tag(text)
            for i in k:
                    if (i[1][:2] == "VB" or i[1][:2] == "JJ") or i[1][:2] == "RB":
                        t = t + i[0] + ' '

                    x.append(t)
                    filename = "pos_tagged_" + username + ".txt"
                    handle = open(filename, "w")
                    for i in x:
                        handle.write(i + '\n')

#Function to expand the dictionary:
def learn(name):
    list = []
    filename = 'data_emotions_words_list.csv'
    fname = 'new_dict.csv'
    #########################
    fname = 'a.csv'
    ##########################
    dict_list = []
    new_list = []
    l = 0
    oh = []
    oa = []
    os = []
    od = []
    of = []
    oc = []

##FILENAME CHANGED ORIGINAL == fname

    with open(fname,encoding="ISO-8859-1",newline='') as n:
            #new dictionary
        new_reader = csv.reader(n)
        for new_row in new_reader:
            my_new_list = new_row
                #new_list.append(my_new_list[0])
            dict_list.append(my_new_list[0])
            oh.append(float(my_new_list[1]))
            oa.append(float(my_new_list[2]))
            os.append(float(my_new_list[3]))
            of.append(float(my_new_list[4]))
            od.append(float(my_new_list[5]))
            oc.append(float(my_new_list[6]))
            print(dict_list[l]+","+str(oh[l]))
            l += 1

    list_evalue = []
    my_new_list = []
    b = []
    j = 0

    ##############ADDED#########
    a = []
    h = []
    s = []
    d = []
    f = []
    c =[]
    dh = []
    da = []
    ds = []
    dd = []
    df = []
    dc = []

    #####################################

    words = []
    ans = [0.52,0.32,0.3,0.36,0.28]
    '''
    ans[0] = 0.48
    ans[1] = 0.32
    ans[2] = 0.3
    ans[3] = 0.36
    ans[4] = 0.28
    '''
    fi = open(name,'r')
    tweets = fi.readlines()
    for tweet in tweets:
        if(tweet == '\n'):
            continue
            words[:] = []
            words = tweet.split(' ')
            for word in words:
                if(word == '\n'):
                    continue
                #print(word)
                word=word.lower()
                with open(filename,encoding="ISO-8859-1",newline='') as di:  #original dictionary
                    reader = csv.reader(di)
                    for row in reader:
                        my_list=row
                        if(word != my_list[0]):                     # word not in original dictionary

                            if(word in new_list):
                                if(word in dict_list):              # word in new dictionary and in tweet
                                    continue
                                else:
                                    j = new_list.index(word)        # repeated words
                                    c[j] += 1
                            else:
                                l += 1
                new_list.append(word)               # word not in new dictionary
                oh.append(ans[0])
                oa.append(ans[1])
                os.append(ans[2])
                of.append(ans[3])
                od.append(ans[4])
                oc.append(1)

                                #print(new_list[l-1]+","+str(h[l-1])+","+str(a[l-1])+","+str(s[l-1])+","+str(f[l-1])+","+str(d[l-1])+","+str(c[l-1]))


    total = l
    z = 0
    '''
    cnt = 0
    with open(fname,encoding="ISO-8859-1",newline='') as n: #new dictionary
    new_reader = csv.reader(n)
    fornew_row in new_reader:
    cnt += 1
    '''

    while(z<len(new_list)):
        if(c[z]>=1000):
            c[z] = round((c[z]/1036),1)
            z = z + 1


    print("\n"+str(len(dict_list))+"\n")
    print(len(new_list))
    print("\n")
    print(l)
    i = 0

    k = 0
    z = 0
    '''
        flag2 = []
    while(i<len(dict_list)):
    flag2[i] = 0
    i += 1
    '''
    flag2 = [0]*len(dict_list)
    flag3 = [0]*len(new_list)
    while(z < len(new_list)):
        i = 0
        flag = 0
        while(i<len(dict_list) and flag == 0):
            if(new_list[z] == dict_list[i] and flag3[z] == 0):        # in tweet and in dictionary
                flag = 1
                flag2[i] = 1
                flag3[z] = 1
                list.append(new_list[z])
                dh.append((h[z]*c[z] + oh[i]*oc[i])/(c[z]+oc[i]))
                da.append((a[z]*c[z] + oa[i]*oc[i])/(c[z]+oc[i]))
                ds.append((s[z]*c[z] + os[i]*oc[i])/(c[z]+oc[i]))
                df.append((f[z]*c[z] + of[i]*oc[i])/(c[z]+oc[i]))
                dd.append((d[z]*c[z] + od[i]*oc[i])/(c[z]+oc[i]))
                dc.append(c[z]+oc[i])

            else:
                if(flag2[i] == 0):                                    # only in dictionary
                    list.append(dict_list[i])
                    dh.append(oh[i])
                    da.append(oa[i])
                    ds.append(os[i])
                    df.append(of[i])
                    dd.append(od[i])
                    dc.append(oc[i])
                    flag2[i] = 1
                    i += 1

            if(flag == 0 and flag3[z] == 0):
                list.append(new_list[z])
                dh.append(h[z])                     # in tweet only
                da.append(a[z])
                ds.append(s[z])
                df.append(f[z])
                dd.append(d[z])
                dc.append(c[z])
            #print(list[z]+","+str(dh[z])+","+str(da[z])+","+str(ds[z])+","+str(df[z])+","+str(dd[z])+","+str(dc[z]))
                z += 1
    z = 0
    y = open("new_dict.csv",'w')
    while(z < len(list)):
        print(list[z]+","+str(dh[z])+","+str(da[z])+","+str(ds[z])+","+str(df[z])+","+str(dd[z])+","+str(dc[z]))
        y.write(list[z]+","+str(dh[z])+","+str(da[z])+","+str(ds[z])+","+str(df[z])+","+str(dd[z])+","+str(dc[z]))
        y.write("\n")
        z = z + 1
    y.close()

#Main Program:
def run(username, master):
    column0_padx = 24
    row_pady = 36
    tweets = []
    print (username)
    if(username[0] == "@"):
        tweets = get_all_tweets(username)
        print("Downloading of tweets of user has started !!")



    if(username[0] == "#"):
        tweets = get_all_hash(username)
        print("Downloading of tweets of hashtag has started !!")

    print("Tweets have been downloaded !!")
    print("Now Cleaning of tweets starts !!")

        #time.sleep(1)
    '''
    filename = username+"tweets.txt"

    with open(filename) as f:
    for line in f:
    tweets.append(line)
    '''

    tweets=rem_substring(tweets,'#')
    tweets=rem_substring(tweets,'http')
    tweets=rem_substring(tweets,'@')
    tweets=rem_substring(tweets,'RT')
    tweets=rem_punctuation(tweets,'\"')
    tweets=rem_punctuation(tweets,'-')
    tweets=rem_punctuation(tweets,'!')
    tweets=rem_punctuation(tweets,':')
    tweets=removeNonEnglish(tweets)
        #tweets.replace("."," ")
    for tweet in tweets:
        tweet=tweet.replace("."," ")


    z=open('cleaned_'+username+'.txt','w')
    for tweet in tweets:
        tweet=tweet.encode('ascii','ignore')
        z.write("\n")
        z.write(tweet.decode())
    z.close()
        #filename = username+"_cleaned_tweets.txt"
        #x = open(filename,"a")
    '''for i in tweets:
    x.write(i+'\n')
        #time.sleep(2)
    '''
    POS_tagger(tweets,username)
    print("Tweets have now been cleaned !!")
    evalue = score(tweets)

    learn("pos_tagged_"+username+".txt")
    L3 = Label(master, text="Happiness : ", wraplength=150, justify='left', pady=row_pady)
    L3.grid(row=5, column=0, sticky='w', padx=column0_padx)
    L8 = Label(master, text=str(evalue[0]))
    L8.grid(row=5, column=1, sticky='w')
    L4 = Label(master, text="Anger : ", wraplength=150, justify='left', pady=row_pady)
    L4.grid(row=6, column=0, sticky='w', padx=column0_padx)
    L9 = Label(master, text=str(evalue[1]))
    L9.grid(row=6, column=1, sticky='w')
    L5 = Label(master, text="Sadness : ", wraplength=150, justify='left', pady=row_pady)
    L5.grid(row=7, column=0, sticky='w', padx=column0_padx)
    L10 = Label(master, text=str(evalue[2]))
    L10.grid(row=7, column=1, sticky='w')
    L6 = Label(master, text="Fear : ", wraplength=150, justify='left', pady=row_pady)
    L6.grid(row=8, column=0, sticky='w', padx=column0_padx)
    L11 = Label(master, text=str(evalue[3]))
    L11.grid(row=8, column=1, sticky='w')
    L7 = Label(master, text="Disgust : ", wraplength=150, justify='left', pady=row_pady)
    L7.grid(row=9, column=0, sticky='w', padx=column0_padx)
    L12 = Label(master, text=str(evalue[4]))
    L12.grid(row=9, column=1, sticky='w')

    bottom_fram = Frame(master)
    bottom_fram.grid(row=10, column=0, columnspan=2, sticky='w')

    btn_start = ttk.Button(bottom_fram, text = "Show Graph", width=20, command= lambda: new_window())
    btn_start.pack(side='left', padx=145)
    print("Tweets have now been cleaned !!")

    def new_window():
        id = "Graph"
        window = Toplevel(master=None)#Removed passing of master
        label = ttk.Label(window, text=id)
        label.pack(side="top", fill="both", padx=10, pady=10)

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
                    #t = arange(0.0,3.0,0.01)
                    #s = sin(2*pi*t)
                    #a.plot(t,s)
        a.plot([1,2,3,4,5],[evalue[0], evalue[1], evalue[2], evalue[3], evalue[4]])
        a.set_title('Emotion Scores')
        a.set_xlabel('1 - > Happiness , 2 - > Anger , 3 - > Sadness , 4 - > Fear , 5 - > Disgust ')
        a.set_ylabel('Score')

                    # atk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=window)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2TkAgg( canvas, window )
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        def on_key_event(event):
            print('you pressed %s'%event.key)
            key_press_handler(event, canvas, toolbar)

            canvas.mpl_connect('key_press_event', on_key_event)

        def _quit():
            window.quit()     # stops mainloop
            window.destroy()  # this is necessary on Windows to prevent
                                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

            button = ttk.Button(master=window, text='Quit', command=_quit)
            button.pack(side=BOTTOM)

class App:
    def __init__(self, master):
        self.root = Frame(master)
        column0_padx = 24
        row_pady = 36

                        #Label entry
        userart = Label(
        master, text="Input User Name -> ",
        wraplength=150, justify='left', pady=row_pady)
        entry_point = Entry(master, width=30)
        userart.grid(row=1, column=0, sticky='w', padx=column0_padx)
        entry_point.grid(row=1, column=1, sticky='w')

                        # version
        lbl_version = ttk.Label(master, text="Beta-Version @TechnoDesign")
        version = ttk.Label(master, text="ver. 1.004")
        lbl_version.grid(row=4, column=0, sticky='w', padx=column0_padx)
        version.grid(row=4, column=1, sticky='w')

        sep = ttk.Label(master)
        sep.grid(row=3, column=0, sticky='w')

                        #progress_bar
                        #progressbar = ttk.Progressbar(orient='horizontal', length=200, mode='determinate')
                        #progressbar.grid(row=5, column=0, sticky='w', padx=column0_padx)
                        #progressbar.start()

                        # buttons
        bottom_frame = Frame(master)
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky='w')

        btn_start = ttk.Button(bottom_frame, text = "Run", width=7, command=lambda: run(entry_point.get(), master))
        btn_start.pack(side='left', padx=100)
        btn_exit = ttk.Button(bottom_frame, text="Exit", width=7, command=self.root.quit)
        btn_exit.pack(side='left', padx=10)

def main():
    root = Tk()
    root.title("Emotion Calculator of TWITTER Data")
    root.minsize(500, 700)
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
