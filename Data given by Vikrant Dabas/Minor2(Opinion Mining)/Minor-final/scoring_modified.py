import csv, sys
filename = 'data_emotions_words_list.csv'
global count_adj
global count
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

r=open(sys.argv[1],'r')
for line in r.readlines():
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
                    		ans[0]+=float(my_list[1])*float(special_score)
                    		ans[1]+=float(my_list[3])*float(special_score)
                    		ans[2]+=float(my_list[5])*float(special_score)
                    		ans[3]+=float(my_list[7])*float(special_score)
                    		ans[4]+=float(my_list[9])*float(special_score)
                    	else:
                    		ans[0]+=5-float(my_list[1])
                    		ans[1]+=5-float(my_list[3])
                    		ans[2]+=5-float(my_list[5])
                    		ans[3]+=5-float(my_list[7])
                    		ans[4]+=5-float(my_list[9])
                    special_word=None
                    #final_list.append(ans_list)
                    print(ans_list)
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

                    print(ans_list)
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
                    
                    print(ans_list)
                    break

           
#print(count)
#print(ans)
for i in range(0,5):
    #ans[i]=ans[i]/((5*count_adj)+count)
    ans[i]=ans[i]/(5*count_adj)

print(ans)        
        
