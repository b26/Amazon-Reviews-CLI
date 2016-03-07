import os
from sys import argv

#Remove files
os.system("rm -rf *.idx")
os.system("rm -rf reviews_*")
os.system("rm -rf rterms*")
os.system("rm -rf pterms*")
os.system("rm -rf scores*")

os.system('clear')
#run reviews.py and create reviews_sorted.txt

print("#######################")
print("Creating Phase 1 Files")
print("#######################")

reviews = os.system("python3 reviews.py %s" % argv[1])

if reviews == 0:
    print("reviews_sorted.txt created")
else:
    print("ERROR - reviews_sorted.txt")


pterms = os.system("python3 _pterms.py %s" % argv[1])

if pterms == 0:
    print("pterms.txt created")
else:
    print("ERROR - pterms.txt")

rterms = os.system("python3 _rterms.py %s" % argv[1])

if pterms == 0:
    print("rterms.txt created")
else:
    print("ERROR - rterms.txt")

scores = os.system("python3 _scores.py %s" % argv[1])

if pterms == 0:
    print("scores.txt created")
else:
    print("ERROR - scores.txt")

print()
print()
print("#################################")
print("Creating Phase 2 - Sorting Files")
print("#################################")

sorted_files = ["reviews_sorted.txt"]

pterms_sorted = os.system("sort -u -o pterms_sorted.txt pterms.txt")
if pterms_sorted == 0:
    print("pterms_sorted.txt created")
    sorted_files.append("pterms_sorted.txt")
else:
    print("ERROR - pterms_sorted.txt")

rterms_sorted = os.system("sort -u -o rterms_sorted.txt rterms.txt")

if rterms_sorted == 0:
    print("rterms_sorted.txt created")
    sorted_files.append("rterms_sorted.txt")
else:
    print("ERROR - rterms_sorted.txt")

scores_sorted = os.system("sort -u -o scores_sorted.txt scores.txt")

if scores_sorted == 0:
    print("scores_sorted.txt created")
    sorted_files.append("scores_sorted.txt")
else:
    print("ERROR - scores_sorted.txt")

print()
print()
print("####################################")
print("Creating Phase 2 - Creating Indexes")
print("####################################")

dbload_files = []

for fp in sorted_files:
    oldfile = fp.split('_')[0]
    newfile = oldfile + "_loaded.txt"
    load = os.system("perl break.pl < %s > %s" % (fp, newfile))
    dbload_files.append(newfile)

for fp in dbload_files:
    #db_load -T -t btree -c duplicates=1 -f file.txt newfile.idx
    if 'reviews' in fp:
        dbload = os.system("db_load -T -t hash -f %s rw.idx" % (fp))
        print("rw.idx created.")
    elif 'pterms' in fp:
        dbload = os.system("db_load -T -t btree -c duplicates=1 -f %s pt.idx" % (fp))
        print("pt.idx created.")
    elif 'rterms' in fp:
        dbload = os.system("db_load -T -t btree -c duplicates=1 -f %s rt.idx" % (fp))
        print("rt.idx created.")
    elif 'scores' in fp:
        dbload = os.system("db_load -T -t btree -c duplicates=1 -f %s sc.idx" % (fp))
        print("sc.idx created.")
    else:
        print("DBLOAD Error reading %s" % (fp))

print()
print()
