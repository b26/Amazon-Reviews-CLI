from bsddb3 import db
#Get an instance of BerkeleyDB
DATABASE='Oscar2015.db'
# Create a new databaseof type HASH 
database = db.DB()
database.set_flags(db.DB_DUP)
database.open(DATABASE, None, db.DB_BTREE, db.DB_CREATE)
#Get cursor object
cur = database.cursor()
#(key,data) pair

cur.put(b'Best Picture', "The Imitation Game",db.DB_KEYFIRST)
cur.put(b'Best Actress', "Marion Cotillard",db.DB_KEYFIRST)
cur.put(b'Best Actor', "Robert Duvall",db.DB_KEYFIRST)
cur.put(b'Best Animation', "How to Train Your Dragon 2",db.DB_KEYFIRST)
cur.put(b'Best Actor', "Mark Ruffalo",db.DB_KEYFIRST)
cur.put(b'Best Animation', "Big Hero 6",db.DB_KEYFIRST)
cur.put(b'Best Picture', "Whiplash",db.DB_KEYFIRST)
cur.put(b'Best Actress', "Rosamund Pike",db.DB_KEYFIRST)
cur.put(b'Best Picture', "The Theory of Everything",db.DB_KEYFIRST)
# get all rows inserted into the database
iter = cur.first()
while iter:
 print(iter)
 iter = cur.next()
print('_____________________________')

# get duplicate data at current cursor's place
print(cur.first())
num = cur.count(); #number of duplicate records at the current cursor position
for i in range(1,num):
	print(cur.next_dup())
print('_____________________________')

#get first record for Best Actress
result = database.get(b'Best Actress')
print(result)
print('_____________________________')

#get duplicates data using cursor
print('first duplicate pairs:') 
iter = cur.first()
while iter:
 print(iter)
 iter = cur.next_dup(flags=0, dlen=-1, doff=-1) #If the next key/data pair of the database is a duplicate record for the current key/data pair, the cursor is moved to the next key/data pair of the database, and that pair is returned. The DBcursor->get() method will return DB_NOTFOUND if DB_NEXT_DUP is set and the next key/data pair of the database is not a duplicate data record for the current key/data pair.

print('second duplicate pairs:')
iter = cur.next() # go to the next record ( which is not a duplicate record for the previous key/data pair)
while iter:
 print(iter)
 iter = cur.next_dup(flags=0, dlen=-1, doff=-1) # get the duplicat records of current key

print('third duplicate pairs:')
iter = cur.next() # go to the next record
while iter:
 print(iter)
 iter = cur.next_dup(flags=0, dlen=-1, doff=-1) # get the duplicat records of current key

print('fourth duplicate pairs:')
iter = cur.next() # go to the next record
while iter:
 print(iter)
 iter = cur.next_dup(flags=0, dlen=-1, doff=-1) # get the duplicat records of current key


cur.close()
database.close()
