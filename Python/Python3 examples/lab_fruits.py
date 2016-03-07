from bsddb3 import db
#Get an instance of BerkeleyDB
DATABASE='fruit_example.db'
# Create a new databaseof type HASH 
database = db.DB()
database.open(DATABASE, None, db.DB_HASH, db.DB_CREATE)
#Get cursor object
cur = database.cursor()
#(key,data) pair
cur.put(b'apple', "red",db.DB_KEYFIRST)
database.put(b'pear', "green")
# get all rows inserted into the database
iter = cur.first()
while iter:
 print(iter)
 iter = cur.next()
print("------------------------")
#get only a specific row
# get only the data at that key: searching using the database object
result = database.get(b'pear')
#Will give b'green'
print(result)
# removing from the database
# using database object
database.delete(b'apple')
iter = cur.first()
while iter:
 print(iter)
 iter = cur.next()
print("------------------------")
# using cursor
cur.put(b'zat', "xat",db.DB_KEYFIRST)
iter = cur.first()
while iter:
 print(iter)
 iter = cur.next()
print("------------------------")
cur.delete() # deletes the key-data pair currently referenced by the cursor
iter = cur.first()
while iter:
 print(iter)
 iter = cur.next()
print("------------------------")

cur.close()
database.close()

##
#(b'apple', b'red')
#(b'pear', b'green')
#------------------------
#b'green'
#(b'pear', b'green')
#------------------------
#(b'pear', b'green')
#(b'zat', b'xat')
#------------------------
#(b'pear', b'green')
#------------------------
#
