#python3 b2.py
from bsddb3 import db
#Get an instance of BerkeleyDB
DATABASE='duplicate.db'
# Create a new database of type HASH 
database2 = db.DB()
database2.set_flags(db.DB_DUP)
database2.open(DATABASE, None, db.DB_HASH, db.DB_CREATE)
#Get cursor object
cur = database2.cursor()
#(key,data) pair
database2.put(b'red', "apple")
cur.put(b'green', "pear",db.DB_KEYFIRST)
cur.put(b'yellow', "grapefruit",db.DB_KEYFIRST)
cur.put(b'blue', "berry",db.DB_KEYFIRST)
cur.put(b'blue', "lemon",db.DB_KEYFIRST)
# get all rows inserted into the database
iter = cur.first()
while iter:
 print(iter)
 iter = cur.next()
cur.first()
print(cur.count())
print(cur.next_dup())
#print(result)
cur.close()
database2.close()

# Output: 
#(b'blue', b'lemon')
#(b'blue', b'berry')
#(b'yellow', b'grapefruit')
#(b'green', b'pear')
#(b'red', b'apple')
#2
#(b'blue', b'berry')
#

