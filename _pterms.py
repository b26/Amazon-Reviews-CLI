import re
from sys import argv
fp = open(argv[1], "r")

output = fp.readlines()
reg = re.compile('\w{3,}')
terms = []
count = 1
for line in output:
    if line != ['\n']:
        if "/title:" in line:
            line = line[15:]
            term = reg.findall(line)
            for word in term:
                word = str(word).lower()
                terms.append([word, str(count)])
            count += 1
f = open('pterms.txt', 'w')
for term in terms:
    term = ','.join(term) + '\n'
    f.write(term)
f.close()
fp.close()
