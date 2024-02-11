ab = open('abbrev.txt', 'w')

lis = list()
with open('abbreviations.txt', encoding='utf-8') as f:
    reader = f.readlines()
    for i in reader:
        i = i.replace(' – ', ';')
        i = i.split('.')
        lis.append(i[1].strip())


for i in lis:
    ab.write(i + '\n')