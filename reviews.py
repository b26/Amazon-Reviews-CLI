from sys import argv
fp = open(argv[1], "r")
output = fp.readlines()
lines = ""
count = 1
for line in output:
    split = line.replace('"', '&quot;').replace('\\' , '\\\\')
    if split != ['\n']:
        if "/title:" in split:
            string = '"%s"' % (split[15:].rstrip('\n'))
        elif "/productId:" in split:
            string = "\n" + str(count) + "," + split[19:].rstrip('\n') + ","
            count += 1
        elif "/userId:" in split:
            split = split[15:]
            string = "," + split.rstrip('\n')
        elif "/profileName:" in split:
            split = split[20:]
            string = ',"%s"' % (split.rstrip('\n'))
        elif "/helpfulness:" in split:
            string = "," + split[20:].rstrip('\n')
        elif "/time:" in split:
            string = "," + split[13:].rstrip('\n')
        elif "/score:" in split:
            string =  "," + split[14:].rstrip('\n')
        elif "/summary:" in split:
            string = ',"%s",' % (split[16:].rstrip('\n'))
        elif "/price:" in split:
            string = "," + split[15:].rstrip('\n')
        elif "/text:" in split:
            string = '"%s"' % (split[13:].rstrip('\n'))
        lines += string

f = open('reviews_sorted.txt', 'w')
f.write(lines[1:])
f.close()
fp.close()
