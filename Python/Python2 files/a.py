import bsddb
# Creatig a database
DATABASE = 'cstudents.db'
# Making it with BTree organization
db = bsddb.btopen(DATABASE,'c')
# Inserting a record
Sid = '123'
Name = 'James'
db[Sid] = Name
#Obtaining the result for a query
if (db.has_key(Sid)==True):
	sname = db[Sid]
	print(sname)
# Deleting a record
del db[Sid]
db.sync()
# Closing the connection
db.close()

