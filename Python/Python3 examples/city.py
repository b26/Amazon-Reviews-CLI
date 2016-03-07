# the Berkeley db database
from bsddb3 import db                   
filename = 'city.db'
# Get an instance of BerkeleyDB 
cityDB = db.DB()
# Create a database in file "city" using Hash access method
cityDB.open(filename, None, db.DB_HASH, db.DB_CREATE)
# Insert 3 elements in database 

cityDB.put(b'Edmonton',"AB")
cityDB.put(b'Calgary',"AB")
cityDB.put(b'Camrose',"AB")

# Close database
cityDB.close()

# Open database and write its contents 
# Open database
cityDB = db.DB()

# Access method: Hash
# set isolation level to "dirty read (read uncommited)"
cityDB.open(filename, None, db.DB_HASH, db.DB_DIRTY_READ)
# get database cursor and print out database content
cursor = cityDB.cursor()
rec = cursor.first()
while rec:
        print (rec)
        rec = cursor.next()
cityDB.close()