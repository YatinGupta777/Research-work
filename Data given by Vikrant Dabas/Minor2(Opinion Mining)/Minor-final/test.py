import nltk
nltk.download('punkt')
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
POS_tagger(tweets)
