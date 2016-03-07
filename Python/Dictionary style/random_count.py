#!/usr/bin/env python3

import bsddb3
import os.path
import random

# Create the database
if os.path.isfile("random.db"):
    db = bsddb3.hashopen("random.db", "w")
else:
    db = bsddb3.hashopen("random.db", "c")

# Populate the database
i = 100
while i > 0:
    key = "".join([str(chr(97 + random.randrange(0, 26))) for _ in range(64 + random.randrange(0, 64))]).encode()
    value = "".join([str(chr(97 + random.randrange(0, 26))) for _ in range(64 + random.randrange(0, 64))]).encode()
    if db.get(key) is None:
        db[key] = value
        i -= 1

# Get the number of records in the database
cursor = db.db.cursor()
i = 0
try:
    record = cursor.first()
    i += 1
except bsddb3.db.DBNotFoundError:
    pass
else:
    while True:
        try:
            record = cursor.next()
            i += 1
        except bsddb3.db.DBNotFoundError:
            break
cursor.close()
print(i)
