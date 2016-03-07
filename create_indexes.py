import re

fp = open('reviewst.txt', "r")
f = open('rw.txt', "w")
lines = fp.readlines()
reg = re.compile('([^,]+),(.*?)$')
pairs = []
for line in lines:
    pair = reg.findall(line)[0]
    key = str(pair[0])
    data = str(pair)
    #pairs.append([key, data])
    f.write(key)
    f.write('\n')
    f.write(data)
    f.write('\n')
    #f.write(str(pair))
for pair in pairs:
    key = pair[0]
    #f.write(key)
    #f.write('\n')

for pair in pairs:
    data = pair[1]
    #f.write(data)
    #f.write('\n')

fp.close
f.close()

