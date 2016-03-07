from sys import argv
fp = open(argv[1], "r")
output = fp.readlines()
terms = []
count = 1
for line in output:
    if line != ['\n']:
        if "/score:" in line:
            term = line[14:].rstrip('\n')
            terms.append([term, str(count)])
            count += 1
f = open('scores.txt', 'w')
for term in terms:
    term = ','.join(term) + '\n'
    f.write(term)
f.close()
fp.close()
