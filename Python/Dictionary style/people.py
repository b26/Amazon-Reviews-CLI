#!/usr/bin/env python3

import bsddb3
import os.path

# Create the database
if os.path.isfile("people.db"):
    db = bsddb3.btopen("people.db", "w")
else:
    db = bsddb3.btopen("people.db", "c")

# Add data to the database
data = {b'Ian': 'Smith', b'Carl': 'Horwitz', b'Ted': 'Smith', b'Fred': 'Torrens'}
for key, value in data.items():
    db[key] = value

# Find the last name of 'Carl'
print(db.get(b'Carl').decode(), end="\n\n")

# Find everyone with the last name 'Smith'
cursor = db.db.cursor()
try:
    record = cursor.first()
except bsddb3.db.DBNotFoundError:
    pass
else:
    if record[1].decode() == 'Smith':
        print(record[0].decode())
    while True:
        try:
            record = cursor.next()
            if record[1].decode() == 'Smith':
                print(record[0].decode())
        except bsddb3.db.DBNotFoundError:
            break
cursor.close()

# Close the database
db.close()
