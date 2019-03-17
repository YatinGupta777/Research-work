import csv, sys
filename = 'data_emotions_words_list.csv'
r=open('sample','r')
w=open('corrected_words','a')

for line in r.readlines():
    line=line.lower()
    line=line.split(" ")
    list_words=line
    #print(list_words[0])
    for word in list_words:
        with open(filename,encoding="ISO-8859-1",newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                my_list=row
                if (word == my_list[0] and word[0]==my_list[0][0]):
                    break
            new_word=input("Enter the correct word for %s" %word)
            print(new_word)
            w.write(new_word)

w.close()
