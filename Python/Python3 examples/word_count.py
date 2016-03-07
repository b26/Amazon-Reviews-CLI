from bsddb3 import db


DATABASE = 'word_count.db'
database = db.DB()
database.open(DATABASE, None, db.DB_BTREE, db.DB_CREATE)

# instantiate the cursor
cur = database.cursor()


# load the data into the database
data = [(b'hello', "4"), (b'hola', "7"), (b'bonjour', "2"),
        (b'be', "9"), (b'ser', "3"), (b'estar', "7"), (b'etre', "2")]
for datum in data:
    cur.put(datum[0], datum[1], db.DB_KEYFIRST)


# Obtaining one piece of metadata
num_entries = len(database)
print("We have %i entries in our BTree!\n" % num_entries)


# Get all kinds of metadata
meta = database.stat()
print("Here is some metadata!")
print(meta)
print('-' * 40)
print()


# Get the data by iterating over the cursor
entries = [cur.first()]
for i in range(num_entries - 1):
    entries.append(cur.next())


# Get all values using "get"
entries_2 = []
for word in data:
    entries_2.append(int(database.get(word[0])))


# Check they are the same length visually
print("Data obtained via the cursor: %s" % str(entries))
print("Data obtained via DB().get(): %s" % str(entries_2))


# close the cursor
cur.close()


# write to disk
database.sync()


# close the database connection
database.close()
print('-' * 40)


# PART 2
database = db.DB()
database.open(DATABASE, None, db.DB_BTREE, db.DB_CREATE)
print("We still have %i entries in our BTree!\n" % len(database))


# empty database
database.truncate()
database.close()
print('-' * 40)


# PART 3
database = db.DB()
database.open(DATABASE, None, db.DB_BTREE, db.DB_CREATE)
print("We have %i entries in our BTree!\n" % len(database))
database.close()
