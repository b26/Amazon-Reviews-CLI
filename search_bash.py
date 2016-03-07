from bsddb3 import db
import os
import sys
review_db = db.DB()
review_db.open("rw.idx")
review_cur = review_db.cursor()
idSet = set()

def query(string):
    #checks if an index is provided. if not assign
    #a to index. 'a' signifies it will check all indexes.
    rscore = "rscore" in string
    pprice = "pprice" in string
    rdate = "rdate" in string
    if rscore or pprice or rdate:
       string = string.split()
       first = string[0]
       second = string[1]
       third = string[2]
    else:
        if string[0] == 'p' or string[0] == 'r':
            first = string[0]
        else:
            first = "a"
        #if '%' exists lets save it. we do not need it though
        third = '%' if string[-1] == '%' else None
        #if index equals all then we need to choose the correct
        #range of chars to select
        if first == "a":
            second = string[:-1] if third else string
        else:
            second = string[2:-1] if third else string[2:]
    query = (first, second, third)
    return query

def search(string, idSet):
    string = string.split()
    queries = []
    if string[0] == "rscore":
        find("sc.idx", string)
    else:
        for i in range(len(string)):
            if string[i] not in '><[]' and not string[i].isdigit():
                rscore = "rscore" in string[i]
                pprice = "pprice" in string[i]
                rdate = "rdate" in string[i]
                if rscore  or pprice or rdate:
                    text = string[i] + " " + string[i+1] + " " + string[i+2]
                else:
                    text = string[i]
                queries.append(query(text))
        #TODO split point should be here.
        for data in queries:
            print("data", data)
            index = data[0]
            text = data[1]
            like = data[2]
            if index == "p":
                run("pt.idx", index, text, idSet, like)
            elif index == "r":
                run("rt.idx", index, text, idSet, like)
            elif index == "a":
                run("pt.idx", index, text, idSet, like)
                run("rt.idx", index, text, idSet, like)
    idSet = sorted(idSet)
    print(idSet)
    #runr(idSet)

#this function handles opening and closing the database. naming convention needs to be reviewed.
def run(fp, index, text, idSet, like):
        temp_db = db.DB()
        temp_db.open(fp)
        cursor = temp_db.cursor()
        data = cursor.first()
        while data:
            title = data[0].decode("utf-8")
            _id = data[1]
            if like:
                if text in title:
                    idSet.add(_id)
            else:
                if text == title:
                    idSet.add(_id)
            data = cursor.next()
        cursor.close()
        temp_db.close()

def find(fp, string):
    condition = string[1]
    value = float(string[2])
    temp_db = db.DB()
    temp_db.open(fp)
    #scores = []
    cursor = temp_db.cursor()
    data = cursor.first()
    while data:
        temp_value = float(data[0].decode("utf-8"))
        if condition == ">":
            if temp_value > value:
                print(data)
                #scores.append(int(data[1].decode("utf-8")))
        elif condition == "<":
            if temp_value < value:
                print(data)
        data = cursor.next()
    #print(sorted(scores))
    cursor.close()
    temp_db.close()

"""
def runr(idSet):
    for _id in idSet:
        review = review_db.get(_id)
        #print(review)
"""

def menu():
    os.system('clear')
    print("#################")
    print("BerkeleyDB Search")
    print("#################")
    print()

quit = False

while not quit:
    menu()
    queries = input("> ")
    if queries:
        search(queries, idSet)
        choice = input("press any button to continue or q for quit ")
        idSet = set()
        if choice == "q":
            quit = True
    else:
        quit = False

os.system('clear')
review_cur.close()
review_db.close()
sys.exit()

