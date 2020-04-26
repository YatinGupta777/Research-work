
import tweepy
from time import sleep
import csv
import nltk
from tkinter import*
import tkinter as ttk
from twitter import *
import twitter

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler

from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

consumer_key = "RGVO3CTujE60TW5IQy1JwmyxF"
consumer_secret = "ziWzApZCAqlwOt3xK3L0B02VjEsDFZg4Fniy76TsTLKgtnjqlG"
access_key = "1587880604-1tjWpdETzVE4fPALCGeNs6O2oHi4y8ShwIsDQSl"
access_token = "1587880604-1tjWpdETzVE4fPALCGeNs6O2oHi4y8ShwIsDQSl"
access_secret = "wJHBahm2y3KnTXuuj2JX18GAolaHVMnLKZ7Ygc0LxnQMH"
access_token_secret = "wJHBahm2y3KnTXuuj2JX18GAolaHVMnLKZ7Ygc0LxnQMH"

number_of_tweets = 5000
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
t = Twitter(
    auth=OAuth(access_key, access_secret, consumer_key, consumer_secret))

#Function to download tweets corresponding to a hash tag.
def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

def get_all_hash(hashtag):

    # Create the api endpoint
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    
    # Mention the maximum number of tweets that you want to be extracted.
    
    maximum_number_of_tweets_to_be_extracted = number_of_tweets
    # Mention the hashtag that you want to look out for
    
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=hashtag,rpp=100).items(maximum_number_of_tweets_to_be_extracted):
        tweets.append((str(tweet.text.encode('utf-8')) + '\n'))
    
    new_file = hashtag + ".txt"
    handle = open(new_file, "w+")
    for i in tweets:
        handle.write(i)
       
    print ('Extracted ' + str(len(tweets)) \
    + ' tweets with hashtag ' + hashtag)    
    return tweets
#print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
#Function to download tweets corresponding to an username.
def get_all_tweets(username):

# Authorization to consumer key and consumer secret 
        extractor = twitter_setup()

# We create a tweet list as follows:
        tweets = extractor.user_timeline(screen_name=username, count=200)
        tweets_list = []
        for i in tweets:
            tweets_list.append(i.text)
        print("Number of tweets extracted: {}.\n".format(len(tweets)))
        return tweets_list

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

def rem_punctuation(tweets):
    #print(len(tweets))
    m=0
    validLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    for i in tweets:
        x = ""
        for j in i:
            if j in validLetters:
                x += j
        tweets[m]=x
        m=m+1
    return tweets

def score(name,username):
    filename = 'data_emotions_words_list.csv'
    stop_words = set(stopwords.words('english')) 
    count=0
    final_ans=[]
    file_string = ""
    test_file_string = ""
    list_words = []
    final_ans.append(0)
    final_ans.append(0)
    final_ans.append(0)
    final_ans.append(0)
    final_ans.append(0)
    special_word=None
    #special_score=0 ###CHANGED FROM NONE
    
        #r=open(sys.argv[1],'r')
    for line in name:
        temp = ''
        ans=[]
        count_adj= 0
        special_word=None
        special_score=0
        ans.append(0)
        ans.append(0)
        ans.append(0)
        ans.append(0)
        ans.append(0)
        line=line.lower()
        line=line.replace("."," ")
        line=line.split(" ")
        list_words=line
      #  print (line)

        for word in list_words:
            with open(filename,encoding="ISO-8859-1",newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    #print(row)
                    my_list = row
                    word = word.lower()
                    if (word == my_list[0] and len(word)>=1):
                        ans_list=[]
                        count_adj +=1
                        temp += word + ' ' 
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
                        #    print(special_word,word)
                        #    print(special_score)
                            if special_score>=0:
                                ans[0]+=float(my_list[1])*max(0.5,float(special_score))
                                ans[1]+=float(my_list[3])*max(0.5,float(special_score))
                                ans[2]+=float(my_list[5])*max(0.5,float(special_score))
                                ans[3]+=float(my_list[7])*max(0.5,float(special_score))
                                ans[4]+=float(my_list[9])*max(0.5,float(special_score))
                                special_score = 0
                                special_word=None
                            else:
                                ans[0]+=5-float(my_list[1])
                                ans[1]+=5-float(my_list[3])
                                ans[2]+=5-float(my_list[5])
                                ans[3]+=5-float(my_list[7])
                                ans[4]+=5-float(my_list[9])
                                special_word=None
                                special_score = 0
                                #final_list.append(ans_list)
                                #print(ans_list)
            #break


            with open('adverb.csv',encoding="ISO-8859-1",newline='') as a:
                reader=csv.reader(a)
                for row in reader:
                    list_adverb=row
                                #print(list_adverb)
                    word=word.lower()
                    if (word == list_adverb[0]):
                        count+=1
                        temp+= word +' ' 
                        ans_list=[]
                        ans_list.append(word)
                        ans_list.append(list_adverb[1])
                        ans_list.append(list_adverb[1])
                        ans_list.append(list_adverb[1])
                        ans_list.append(list_adverb[1])
                        ans_list.append(list_adverb[1])

                #Uncommented below
# =============================================================================
#                         ans[0]+=float(list_adverb[1])
#                         ans[1]+=float(list_adverb[1])
#                         ans[2]+=float(list_adverb[1])
#                         ans[3]+=float(list_adverb[1])
#                         ans[4]+=float(list_adverb[1])
# =============================================================================

                        if special_word is None:
                            special_word=word
                            special_score=float(list_adverb[1])
                        else:
                            special_word=word
                            #changed * to + 
                            special_score=float(special_score)+float(list_adverb[1])

                                            #print(ans_list)
                    #break



            with open('verb.csv',encoding="ISO-8859-1",newline='') as v:
                reader=csv.reader(v)
                for row in reader:
                    list_verb=row
                    word=word.lower()
                                #print(list_adverb)
                    if (word==list_verb[0]):
                        count+=1
                        temp+= word +' ' 
                    

                        ans_list=[]
                        ans_list.append(word)
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])
                        ans_list.append(list_verb[1])

                        if special_word is None:
                            special_word=word
                            special_score=float(list_verb[1])
                        else:
                            special_word=word
                            #changed * to + 
                            special_score=float(special_score)+float(list_verb[1])

                                            #print(ans_list)
        for i in range(0,5):
                    #ans[i]=ans[i]/((5*count_adj)+count)
            if count_adj != 0:
                #print(count_adj)
                ans[i]= ans[i]/(5*count_adj)

        #count_adj = 0
        #temp += str(count_adj)
        final_ans[0] += ans[0]
        final_ans[1] += ans[1]
        final_ans[2] += ans[2]
        final_ans[3] += ans[3]
        final_ans[4] += ans[4] 
        
        #Changing to binary outcomes
        max_value = max(ans)
        max_index = ans.index(max_value)
        output = ""
        if max_index == 0:
            output = "Happiness"
        if max_index == 1:
            output = "Anger"
        if max_index == 2:
            output = "Sadness"
        if max_index == 3:
            output = "Fear"
        if max_index == 4:
            output = "Disgust"
# =============================================================================
#         index = 0
#         for i in ans:
#             if index != max_index:
#                 ans[index] = 0
#             index = index +1    
# =============================================================================
            
        if temp != "":
            file_string += temp.rstrip()+ ","+str(ans[0])+","+str(ans[1])+","+str(ans[2])+","+str(ans[3])+","+str(ans[4])+","+output+"\n"
            count = count + 1
            test_file_string += temp.rstrip() + ","+str(ans[0])+","+str(ans[1])+","+str(ans[2])+","+str(ans[3])+","+str(ans[4])+",?"+"\n"     
    
    new_file = "Binary_final_data_"+ username + ".csv"
    handle = open(new_file, "w+")
    header = "A,B,C,D,E,F,G \n"
    handle.write(header)
    handle.write(file_string)
    
    test_file = "TEST_Binary_final_data_"+ username + ".csv"
    handle = open(test_file, "w+")
    header = "A,B,C,D,E,F,G \n"
    handle.write(header)
    handle.write(test_file_string)
    #print(file_string)
    #print(ans)
    final_ans[0] = final_ans[0]/count
    final_ans[1] = final_ans[1]/count
    final_ans[2] = final_ans[2]/count
    final_ans[3] = final_ans[3]/count
    final_ans[4] = final_ans[4]/count
    return final_ans


#Scoring Module 2

# =============================================================================
# def score2(name):
#         # count_adj=0
#     filename = 'data_emotions_words_list.csv'
#     count = 0
#     ans = []
#     ans.append(0)
#     ans.append(0)
#     ans.append(0)
#     ans.append(0)
#     ans.append(0)
#         # r=open(name,'r')
#     count_adj = 0
#         # count_verb=0
#     adj_ans = []
#     adj_ans.append(0)
#     adj_ans.append(0)
#     adj_ans.append(0)
#     adj_ans.append(0)
#     adj_ans.append(0)
#     adv_ans = []
#     adv_ans.append(0)
#     adv_ans.append(0)
#     adv_ans.append(0)
#     adv_ans.append(0)
#     adv_ans.append(0)
# 
#      # r=open(sys.argv[1],'r')
#     for line in name:
#         line = line.lower()
#         line = line.replace(".", " ")
#         line = line.split(" ")
#         list_words = line
#             #    print(list_words[0])
#         for word in list_words:
#             with open("data_emotions_words_list.csv", encoding="ISO-8859-1", newline='') as f:
#                 reader = csv.reader(f)
#                 for row in reader:
#                     my_list = row
#                     word = word.lower()
#                     if (word == my_list[0] and len(word) >= 1):
#                         ans_list = []
#                         count_adj += 1
#                             # print(count)
#                         ans_list.append(word)
#                         ans_list.append(my_list[1])
#                         ans_list.append(my_list[3])
#                         ans_list.append(my_list[5])
#                         ans_list.append(my_list[7])
#                         ans_list.append(my_list[9])
#                         adj_ans[0] += float(my_list[1])
#                         adj_ans[1] += float(my_list[3])
#                         adj_ans[2] += float(my_list[5])
#                         adj_ans[3] += float(my_list[7])
#                         adj_ans[4] += float(my_list[9])
# 
#                         # final_list.append(ans_list)
#                         # print(ans_list)
#                     #break
# #FILENAME CHANGED ORIGINAL == 'adverb.csv'
# 
#     with open('adverb.csv', encoding="ISO-8859-1", newline='') as a:
#         reader = csv.reader(a)
#         for row in reader:
#             list_adverb = row
#                 # print(list_adverb)
#             word = word.lower()
#             if (word == list_adverb[0]):
#                 count += 1
#                 ans_list = []
#                 ans_list.append(word)
#                 ans_list.append(list_adverb[1])
#                 ans_list.append(list_adverb[1])
#                 ans_list.append(list_adverb[1])
#                 ans_list.append(list_adverb[1])
#                 ans_list.append(list_adverb[1])
#                 adv_ans[0] += float(list_adverb[1])
#                 adv_ans[1] += float(list_adverb[1])
#                 adv_ans[2] += float(list_adverb[1])
#                 adv_ans[3] += float(list_adverb[1])
#                 adv_ans[4] += float(list_adverb[1])
# 
#                     # print(ans_list)
#                 break
# #FILENAME CHANGED ORIGINAL == 'verb.csv'
#     with open('verb.csv', encoding="ISO-8859-1", newline='') as v:
#         reader = csv.reader(v)
#         for row in reader:
#             list_verb = row
# 
#             word = word.lower()
#                  # print(list_adverb)
#             if (word == list_verb[0]):
#                 count += 1
#                 ans_list = []
#                 ans_list.append(word)
#                 ans_list.append(list_verb[1])
#                 ans_list.append(list_verb[1])
#                 ans_list.append(list_verb[1])
#                 ans_list.append(list_verb[1])
#                 ans_list.append(list_verb[1])
#                 adv_ans[0] += float(list_verb[1])
#                 adv_ans[1] += float(list_verb[1])
#                 adv_ans[2] += float(list_verb[1])
#                 adv_ans[3] += float(list_verb[1])
#                 adv_ans[4] += float(list_verb[1])
# 
#                     # print(ans_list)
#                 break
# 
#                     ##########ARBITARY VALUE
#             #count_adj = 3
#                     #############
# 
#             if adj_ans[0] / count_adj > 3:
#                 ans[0] = ((adj_ans[0] / 3.725) + adv_ans[0]) / (count + count_adj)
#             else:
#                 ans[0] = ((adj_ans[0] / 3.725) - adv_ans[0]) / (count + count_adj)
# 
#             if adj_ans[2] / count_adj > 3:
#                 ans[2] = ((adj_ans[2] / 3.4875) + adv_ans[2]) / (count + count_adj)
#             else:
#                 ans[2] = ((adj_ans[2] / 3.4875) - adv_ans[2]) / (count + count_adj)
# 
#             if adj_ans[4] / count_adj > 3:
#                 ans[4] = ((adj_ans[4] / 2.665) + adv_ans[4]) / (count + count_adj)
#             else:
#                 ans[4] = ((adj_ans[4] / 2.665) - adv_ans[4]) / (count + count_adj)
# 
#             if adj_ans[1] / count_adj > 3:
#                 ans[1] = ((adj_ans[1] / 2.5) + adv_ans[1]) / (count + count_adj)
#             else:
#                 ans[1] = ((adj_ans[1] / 2.5) - adv_ans[1]) / (count + count_adj)
# 
#             if adj_ans[3] / count_adj > 3:
#                 ans[3] = ((adj_ans[3] / 2.5) + adv_ans[3]) / (count + count_adj)
#             else:
#                 ans[3] = ((adj_ans[3] / 2.5) - adv_ans[3]) / (count + count_adj)
# 
#     print(ans)
#     return ans
# 
# =============================================================================
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

def stemming(tweets):
    # split into words
    for i in tweets:
        m=0
        tokens = word_tokenize(i)
        # stemming of words
        porter = PorterStemmer()
        stemmed = [porter.stem(word) for word in tokens]
        for word in stemmed:
            tweets[m] += word + " "
        m=m+1    
        
    return tweets   

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
    tweets=rem_punctuation(tweets)
    #tweets=rem_punctuation(tweets,'-')
    #tweets=rem_punctuation(tweets,'!')
    #tweets=rem_punctuation(tweets,':')
    #tweets=rem_punctuation(tweets,',')
    
    tweets = stemming(tweets)
    tweets= removeNonEnglish(tweets)
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
    #POS_tagger(tweets,username)
    print("Tweets have now been cleaned !!")
    evalue = score(tweets,username)
    #print(tweets)
    #learn("pos_tagged_"+username+".txt")
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
    

#WORD,HAP,,ANG,,SAD,,FEA,,DIS,
#,AVG,SD,AVG,SD,AVG,SD,AVG,SD,AVG,SD
    
#https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7210440
#https://www.researchgate.net/publication/236273327_Experimenting_with_Distant_Supervision_for_Emotion_Classification
#https://pyswarms.readthedocs.io/en/latest/examples/feature_subset_selection.html