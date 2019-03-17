from tkinter import Tk, Button, Checkbutton, Label, Entry, Frame, ttk
import tkinter
import tweepy
import csv,sys
from twython import Twython
import sys
import time

#Twitter API credentials

consumer_key = "RGVO3CTujE60TW5IQy1JwmyxF"
consumer_secret = "ziWzApZCAqlwOt3xK3L0B02VjEsDFZg4Fniy76TsTLKgtnjqlG"
access_key = "1587880604-1tjWpdETzVE4fPALCGeNs6O2oHi4y8ShwIsDQSl"
access_secret = "wJHBahm2y3KnTXuuj2JX18GAolaHVMnLKZ7Ygc0LxnQMH"

APP_KEY = consumer_key
APP_SECRET = consumer_secret
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

evalue = []
alltweets = []	#initialize a list to hold all the tweepy Tweets
tweets = []     #store tweets in a list
fname = "data_emotions_words_list.csv"



#The Twitter Application credentials
consumer_key = "RGVO3CTujE60TW5IQy1JwmyxF"
consumer_secret = "ziWzApZCAqlwOt3xK3L0B02VjEsDFZg4Fniy76TsTLKgtnjqlG"
access_key = "1587880604-1tjWpdETzVE4fPALCGeNs6O2oHi4y8ShwIsDQSl"
access_secret = "wJHBahm2y3KnTXuuj2JX18GAolaHVMnLKZ7Ygc0LxnQMH"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)


def get_all_hash(name):
    hashtag = name

    api = tweepy.API(auth)
    print("FYI , the following trending topics are available")
    trends1 = api.trends_place(1)
    trends = set([trend['name'] for trend in trends1[0]['trends']])
    print (trends)
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
    maxTweets = 200 # Some arbitrary large number
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
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break
    z=open(hashtag+'.txt','w')
    for tweet in list_tweets:
        tweet=tweet.encode('ascii','ignore')
        z.write(tweet.decode())
    z.close()
    return list_tweets
    #print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))

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
              #print(i)
        m += 1
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

def get_all_tweets(username):
	
    alltweets = []
    user_timeline = twitter.get_user_timeline(screen_name=username,count=200,include_rts=1)
    alltweets.extend(user_timeline)
    oldest = alltweets[-1]['id'] - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(user_timeline) > 0:
        user_timeline = twitter.get_user_timeline(screen_name=username,count=200,include_rts=1,max_id=oldest)
        alltweets.extend(user_timeline)
        oldest = alltweets[-1]['id']

    tweets = []
    for tweet in alltweets:
        tweets.append(tweet['text'])

    return tweets

    '''f = open(username+'tweets.txt','w')
    print("%s tweets downloaded of %s" %(len(alltweets),username))
    for tweet in alltweets:
        print(tweet['text'])
        f.write(tweet['text'])
        f.write("\n")'''

'''def score(name):
    #count_adj=0
    count=0
    ans=[]
    ans.append(0)
    ans.append(0)
    ans.append(0)
    ans.append(0)
    ans.append(0)
    #r=open(name,'r')
    count_adj=0
    #count_verb=0
    adj_ans=[]
    adj_ans.append(0)
    adj_ans.append(0)
    adj_ans.append(0)
    adj_ans.append(0)
    adj_ans.append(0)
    adv_ans=[]
    adv_ans.append(0)
    adv_ans.append(0)
    adv_ans.append(0)
    adv_ans.append(0)
    adv_ans.append(0)


    #r=open(sys.argv[1],'r')
    for line in name:
        line=line.lower()
        line=line.replace("."," ")
        line=line.split(" ")
        list_words=line
    #    print(list_words[0])
        for word in list_words:
            with open("data_emotions_words_list.csv",encoding="ISO-8859-1",newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    my_list=row
                    word=word.lower()
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
                        adj_ans[0]+=float(my_list[1])
                        adj_ans[1]+=float(my_list[3])
                        adj_ans[2]+=float(my_list[5])
                        adj_ans[3]+=float(my_list[7])
                        adj_ans[4]+=float(my_list[9])

                    #final_list.append(ans_list)
                    #print(ans_list)
                        break

            with open('adverb.csv',encoding="ISO-8859-1",newline='') as a:
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
                        adv_ans[0]+=float(list_adverb[1])
                        adv_ans[1]+=float(list_adverb[1])
                        adv_ans[2]+=float(list_adverb[1])
                        adv_ans[3]+=float(list_adverb[1])
                        adv_ans[4]+=float(list_adverb[1])


                        #print(ans_list)
                        break

            with open('verb.csv',encoding="ISO-8859-1",newline='') as v:
                reader=csv.reader(v)
                for row in reader:
                    list_verb=row

                    word=word.lower()
                    #print(list_adverb)
                    if (word==list_verb[0]):
                        count+=1
                        ans_list=[]
                        ans_list.append(word)
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        adv_ans[0]+=float(list_verb[1])
                        adv_ans[1]+=float(list_verb[1])
                        adv_ans[2]+=float(list_verb[1])
                        adv_ans[3]+=float(list_verb[1])
                        adv_ans[4]+=float(list_verb[1])

                        #print(ans_list)
                        break


    if adj_ans[0]/count_adj >3:
    	ans[0]=((adj_ans[0]/3.725)+adv_ans[0])/(count+count_adj)
    else:
	    ans[0]=((adj_ans[0]/3.725)-adv_ans[0])/(count+count_adj)

    if adj_ans[2]/count_adj >3:
	    ans[2]=((adj_ans[2]/3.4875)+adv_ans[2])/(count+count_adj)
    else:
	    ans[2]=((adj_ans[2]/3.4875)-adv_ans[2])/(count+count_adj)

    if adj_ans[4]/count_adj >3:
	    ans[4]=((adj_ans[4]/2.665)+adv_ans[4])/(count+count_adj)
    else:
	    ans[4]=((adj_ans[4]/2.665)-adv_ans[4])/(count+count_adj)

    if adj_ans[1]/count_adj >3:
	    ans[1]=((adj_ans[1]/2.5)+adv_ans[1])/(count+count_adj)
    else:
	    ans[1]=((adj_ans[1]/2.5)-adv_ans[1])/(count+count_adj)

    if adj_ans[3]/count_adj >3:
	    ans[3]=((adj_ans[3]/2.5)+adv_ans[3])/(count+count_adj)
    else:
	    ans[3]=((adj_ans[3]/2.5)-adv_ans[3])/(count+count_adj)
    return ans
'''

def score(name):
    filename = 'data_emotions_words_list.csv'
    count_adj=0
    count=0
    ans=[]
    ans.append(0)
    ans.append(0)
    ans.append(0)
    ans.append(0)
    ans.append(0)
    special_word=None
    special_score=None

    #r=open(sys.argv[1],'r')
    for line in name:
        line=line.lower()
        line=line.replace("."," ")
        line=line.split(" ")
        list_words=line
        #print(list_words[0])
        for word in list_words:
            with open(filename,encoding="ISO-8859-1",newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    my_list=row
                    word=word.lower()
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
                        if special_word is None:
                            ans[0]+=float(my_list[1])
                            ans[1]+=float(my_list[3])
                            ans[2]+=float(my_list[5])
                            ans[3]+=float(my_list[7])
                            ans[4]+=float(my_list[9])
                        else:
                            print(special_word,word)
                            print(special_score)
                            if special_score >=0:
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
                
            with open('adverb.csv',encoding="ISO-8859-1",newline='') as a:
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
                        if special_word is None:
                            special_word=word
                            special_score=float(list_adverb[1])
                        else:
                            special_word=word
                            special_score=float(special_score)*float(list_adverb[1])

                        #print(ans_list)
                        break
                
            with open('verb.csv',encoding="ISO-8859-1",newline='') as v:
                reader=csv.reader(v)
                for row in reader:
                    list_verb=row
                    word=word.lower()
                    #print(list_adverb)
                    if (word==list_verb[0]):
                        count+=1
                        ans_list=[]
                        ans_list.append(word)
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        #ans[0]+=float(list_verb[1])
                        #ans[1]+=float(list_verb[1])
                        #ans[2]+=float(list_verb[1])
                        #ans[3]+=float(list_verb[1])
                        #ans[4]+=float(list_verb[1])
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
        ans[i]=ans[i]/(5*count_adj)

    print(ans)
    return ans

import nltk
#nltk.download('punkt')
filename="cleaned dceshubhtweets.txt"
tweets=[] #store tweets in a list
with open(filename) as f:
	for line in f:
		tweets.append(line)
def POS_tagger(tweets):
	x=[]
#for each line in tweets list
	for line in tweets:
		tokenized=nltk.sent_tokenize(line)
		t=""
		#for each sentence in the line
		for sent in tokenized:
			#tokenize this sentence
			text=nltk.word_tokenize(sent)
			k=nltk.pos_tag(text)
			for i in k:
				if (i[1][:2]=="VB" or i[1][:2]=="JJ") or i[1][:2]=="RB":
     					t=t+i[0]+"("+i[1][:1]+")"+''
     					
		x.append(t)
	filename="pos_tagged.txt"
	handle=open(filename,"w")
	for i in x:
		handle.write(i+'\n')	
#POS_tagger(tweets)        

def learn():
        list_evalue = []
        my_new_list = []
        b = []
        with open('new_dict.csv','r', newline='') as csvfile:
            for line in csv.reader(csvfile, delimiter=' ', quotechar='|'):
                b = line
                my_new_list.append(b[0])
                list_evalue.append(b[1]+","+b[2]+","+b[3]+","+b[4])
            s = open(name,'r')
            p = 0
            for line in s.readlines():
                line=line.lower()
                line=line.split(" ")
                list_words=line
                #print(list_words[0])
                for word in list_words:
                    with open(fname,encoding="ISO-8859-1",newline='') as t:
                        reader = csv.reader(t)
                        for row in reader:
                            my_list=row
                            if (word != my_list[0]):
                                list_evalue.append(ans[0]+","+ans[1]+","+ans[2]+","+ans[3]+","+ans[4])
                                my_new_list.append(word)
                                p += 1

            list2 = []
            evalue2 = []
            flag = []
            flag[:] = 1
            k = 0
            while (i<p-1):
                if(flag[i] == 0):
                    continue
                sum = []
                sum[0] = list_evalue[i].split(",")[0]
                sum[1] = list_evalue[i].split(",")[1]
                sum[2] = list_evalue[i].split(",")[2]
                sum[3] = list_evalue[i].split(",")[3]
                sum[4] = list_evalue[i].split(",")[4]
                j = i+1
                cnt = 0
                while(j<p):
                    if(my_new_list[i] == my_new_list[j]):
                        flag[i] = 0
                        if(flag[j]):
                            sum[0] += list_evalue[j].split(",")[0]
                            sum[1] += list_evalue[j].split(",")[1]
                            sum[2] += list_evalue[j].split(",")[2]
                            sum[3] += list_evalue[j].split(",")[3]
                            sum[4] += list_evalue[j].split(",")[4]
                            flag[j] = 0
                            list2.append(my_new_list[j])
                            cnt += 1
                if(flag[i]):
                    list2.append(my_new_list[i])
                    evalue2.append(sum[0]+","+sum[1]+","+sum[2]+","+sum[3]+","+sum[4])
                evalue2.append(sum[0]/cnt+","+sum[1]/cnt+","+sum[2]/cnt+","+sum[3]/cnt+","+sum[4]/cnt)
                k += 1

            i = 0
            with open('new_dict.csv', 'w', newline='') as csvfile:
                y = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                while(i<k):
                    y.writerow(list2[i]+evalue2[i])

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
            tweets.append(line)'''

    tweets=rem_substring(tweets,'#')
    tweets=rem_substring(tweets,'http')
    tweets=rem_substring(tweets,'@')
    tweets=rem_substring(tweets,'RT')
    tweets=rem_punctuation(tweets,'\"')
    tweets=removeNonEnglish(tweets)
    #tweets.replace("."," ")
    for tweet in tweets:
        tweet=tweet.replace("."," ")

    

    #filename = username+"_cleaned_tweets.txt"
    #x = open(filename,"a")
    '''for i in tweets:
        x.write(i+'\n')
    #time.sleep(2)'''
    print("Tweets have now been cleaned !!")
    evalue = score(tweets)

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

    btn_start = ttk.Button(bottom_fram, text = "Show Graph", width=20, command=lambda: run2(entry_point.get(), master))
    btn_start.pack(side='left', padx=145)
    print("Tweets have now been cleaned !!")

class App:
    def __init__(self, master):
        self.root = Frame(master)
        column0_padx = 24
        row_pady = 36

        #Label entry
        userart = Label(
            master, text="Input UserName/HashTag ",
            wraplength=150, justify='left', pady=row_pady)
        entry_point = Entry(master, width=30)
        userart.grid(row=1, column=0, sticky='w', padx=column0_padx)
        entry_point.grid(row=1, column=1, sticky='w')

        # version
        lbl_version = ttk.Label(master, text="Beta-Version @TechnoDesign")
        version = ttk.Label(master, text="v.001")
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

root = Tk()
root.title("Hashtag Emotion Calculator")
root.minsize(500, 700)
app = App(root)

root.mainloop()

