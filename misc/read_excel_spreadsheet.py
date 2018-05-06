with open("liste des salariés, retraités - Feuil1.tsv","r",encoding='utf-8') as f :
    data = f.read()



# print(data)
splitD = data.split("\n")
names = []
for item in splitD :
    names.append(item.split("\t"))

# print(names)
finalString = ""
column1 = ""
column2 = ""

inc = 0
for name in names:
    if inc > 0 :
        if inc % 2 != 0 :
            column1 += name[0] +" "+name[1] +"\n"
        else:
            column2 += name[0] +" "+name[1] +"\n"
    inc += 1

print(finalString)
with open("reformatted_list.txt", "w", encoding='utf-8') as f :
    f.write(column1+"\n\n"+column2)

    pass