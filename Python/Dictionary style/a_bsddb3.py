from bsddb3 import db
# Davood's file
# Udated by Kriti for dictionary access in bsddb3
# Command to run: python a_bsddb3.py

# Creatig a database
DATABASE = 'cstudents.db'
# Making it with BTree organization
database2=db.DB()
database2.open(DATABASE, None, db.DB_BTREE, db.DB_CREATE)
# Inserting a record
Sid = b'123'
Name = 'James'
database2[Sid] = Name
sid2 = b'456'
Name = 'John'
database2[sid2] = Name

# using cursor to print
cur = database2.cursor()
iter = cur.first()
while iter:
 print(iter)
 iter = cur.next()

#Obtaining the result for a query
if (database2.has_key(Sid)==True):
	sname = database2[Sid]
	print(sname)

# Deleting a record
del database2[Sid]
database2.sync()

# using cursor to print
cur = database2.cursor()
iter = cur.first()
while iter:
 print(iter)
 iter = cur.next()

# Closing the connection
database2.close()

