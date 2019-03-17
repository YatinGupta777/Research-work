import csv
f=open('language_removed','r')
count=1
mydict={}
for line in f.readlines():
    a=line
    a=a.split(' ')
    for word in a:
        if len(word)>=1 and word!='\n':
            word=word.replace("\n","")
            if word in mydict:
                mydict[word]+=1
            else:
                mydict[word]=1
            #print(mydict)   
    #print(count)
    #count+=1

f.close()
print(mydict)
#w = csv.writer(open("words_count.csv", "w"))
#for key, val in mydict.items():
#    w.writerow([key, val])
with open('words_count.csv', 'w') as csvfile:
    fieldnames = ['word', 'count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key,val in mydict.items():
        writer.writerow({'word': key, 'count': val})

        
    
    

