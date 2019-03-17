#the following function is used to detect the nonEnglish characters
#It returns true when the character is an ASCII character
import sys
def isEnglish(s):
 try:
  s.encode('ascii')
 except UnicodeEncodeError:
  return False
 else:
  return True
import csv,sys,nltk
tweets=[]
filename=sys.argv[1]
tweets=[] #storetweets in a list
with open(filename) as f:
	for line in f:
		tweets.append(line)








#filename is the name of the file we want to clean.Please note, that this file contains only one column, i.e. only tweets

#def rem_rt(tweets):
# m=0;
#iterate over all the tweets in the list
#for i in tweets:
# if i[0]=='R' and i[1]=='T': #if RT exists
#  k=i.find(':') #find the first occurence of :
#  if k!=-1:
#   tweets[m]=i[k+1:] # remove all the char before the : and also the :                      #print the string
#  m=m+1
#return tweets





#tweets.append('@gurmeetsinghs13 Your faith, your trust is sacred to us. Together we will create a world class Delhi. http://t.co/oGgNgjHw9M')
#for i in tweets:
#	print('line')
#	print(i)
#x=open('at_the_rate_removed','w')
#The following function removes the part of the string that contains the substring eg. if
#substring = 'http' , then http://www.google.com is removed, that means, remove until a space is found
def rem_substring(tweets,substring):
       m=0;
       print(len(tweets))
       for i in tweets:
              while i.find(substring)!=-1:
                     k=i.find(substring)
                     d=i.find(' ',k,len(i))
                     if d!=-1: #substring is present somwhere in the middle(not the end of the string)
                            i=i[:k]+i[d:]
                     else: #special case when the substring is present at the end, we needn't append the
                            #substring after the junk string to our result
                            i=i[:k]
                     
              tweets[m]=i #store the result in tweets "list"
              #print(i)
              m=m+1
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
 print(len(tweets))
 m=0
 for i in tweets:
  i=i.replace(punct,'')
  tweets[m]=i
  m=m+1
 return tweets
#The following function removes the stopping words from the tweets
def rem_stoppingword(tweets):
 x=[]
 for line in tweets:
  t=""
  for word in line.split(' '):
   if word in nltk.corpus.stopwords.words('english'):
    pass
   else:
    t=t+word+' '
  print(t)
  x.append(t)
 tweets=x
#The following function is a POS tagger based on the NLTK library
def POS_tagger(tweets):
 for line in tweets:
  print(nltk.pos_tag(line.split()))

#for i in tweets:
#	print(i)
tweets=rem_substring(tweets,'#')
tweets=rem_substring(tweets,'http')
tweets=rem_substring(tweets,'@')
tweets=rem_substring(tweets,'RT')
tweets=rem_substring(tweets,'(1')
tweets=rem_punctuation(tweets,'\"')
tweets=removeNonEnglish(tweets)
#filename=input("Please specify a file name to write ->")
x=open("cleaned "+filename,"w")
for i in tweets:
	x.write(i+'\n')
'''
while 0:
    print("Data Cleaning Module ver 0.1")
    print(">")
    print("1.Print the output to console ")
    print("2.Remove the Non English characters")
    print("3.Remove a substring containing the supplied token")
    print("4.Remove Punctuations")
    print("5.Convert every character of tweets to lowercase")
    print("6.Write Output to a file")
    print("7.Remove Stop Words")
    print("8.Exit")
    choice=input("Enter the option->")
    if choice=="3":
        s=input("Enter the token (e.g. # to remove #tags ->")
        tweets=rem_substring(tweets,s)
    elif choice=="2":
        tweets=removeNonEnglish(tweets)
    elif choice=="1":
        for i in tweets:
            print(i)
    elif choice=="8":
        sys.exit(0)
    elif choice=="4":
        tweets=rem_punctuation(tweets)
    elif choice=="5":
        tweets=lower_case(tweets)
    elif choice=="6":
        filename=input("Please specify a file name to write ->")
        x=open(filename,"w")
        for i in tweets:
            x.write(i+'\n')
    elif choice=="7":
        tweets=rem_stoppingword(tweets)
'''
