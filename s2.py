from bsddb3 import db
import os
import sys
import datetime
import time
import re
def query(string):
    #checks if an index is provided. if not assign
    #a to index. 'a' signifies it will check all indexes.
    rscore = "rscore" in string
    pprice = "pprice" in string
    rdate = "rdate" in string
    if rscore or pprice or rdate:
       string = string.split()
       #first is rscore or pprice or rdate
       first = string[0]
       #second is the condition
       second = string[1]
       #third is the value
       third = string[2]
    #if the string isn't rscore, pprice or rdate then do this
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
    #take the the cleaned values and return them as a tuple
    query = (first, second, third)
    return query

#this splits the query string. this function was added
#to support zero or more spaces in the query
#this specifically handles rscore> 2 rscore > 2 rscore >2
def splitString(string):
    string = re.split('(\s|>|<)', string)
    words = []
    for word in string:
        if word != ' ' and word != '':
            words.append(word)
    return words

#this query takes a string and cleans it
#returns queries as an array
#this was made to handle multiple queries
#for example it will handle r:great p:amazon cam% rscore >2 pprice< 60 etc
def clean_query(string):
    string = splitString(string)
    queries = []
    for i in range(len(string)):
        if string[i] not in '><[]' and not string[i].isdigit():
            rscore = "rscore" in string[i]
            pprice = "pprice" in string[i]
            rdate = "rdate" in string[i]
            if rscore  or pprice or rdate:
                text = string[i].replace(" ", "")
                text = string[i] + " " + string[i+1] + " " + string[i+2]
            else:
                text = string[i]
            queries.append(query(text))
    return queries

#this is the search function. it takes a string in the form of 'camera rscore>2 rscore<5' etc and cleans it
#once it passes through a couple rounds of cleaning it gets passed to the appropriate function(s)
#finally this returns a set of Ids
def search(string):
    queries = clean_query(string)
    stream = set()
    modified = False
    for data in queries:
        index = data[0]
        if index == "p":
            tmp_set = title_review_fetch("pt.idx", data)
            stream = setcombine(stream, tmp_set, modified)
        elif index == "r":
            tmp_set = title_review_fetch("rt.idx", data)
            stream = setcombine(stream, tmp_set, modified)
        elif index == "a":
            tmp_set = set()
            title_tmp_set = title_review_fetch("pt.idx", data)
            text_tmp_set = title_review_fetch("rt.idx", data)
            tmp_set = tmp_set.union(title_tmp_set)
            tmp_set = tmp_set.union(text_tmp_set)
            stream = setcombine(stream, tmp_set, modified)
        elif index == 'rscore':
            tmp_set = rscores("sc.idx", data)
            stream = setcombine(stream, tmp_set, modified)
            modified = True
        elif index == 'rdate':
            tmp_set = dates(data)
            stream = setcombine(stream, tmp_set, modified)
            modified = True
        elif index == 'pprice':
            tmp_set = price(data)
            stream = setcombine(stream, tmp_set, modified)
            modified = True
    print("number of results", len(stream))
    #runr(stream)

#this function handles grabbing p: and r: conditions

def title_review_fetch(fp, data):
        text = data[1].lower()
        like = data[2]
        idSet = set()
        temp_db = db.DB()
        temp_db.open(fp)
        cursor = temp_db.cursor()
        results = cursor.first()
        found = False
        text_key = text.encode("utf-8")
        result = temp_db.get(text_key)
        cursor = temp_db.cursor()
        print(result, cursor.next())

        """
        while results:
            title = results[0].decode("utf-8")
            _id = results[1]
            if like:
                if text == title[0:len(text)]:
                    idSet.add(_id)
            else:
                if text == title:
                    idSet.add(_id)
            results = cursor.next()
        """
        cursor.close()
        temp_db.close()
        return idSet

#this function handles all rscore conditions
#returns scores as a set
def rscores(fp, string):
    condition = string[1]
    value = float(string[2])
    temp_db = db.DB()
    temp_db.open(fp)
    scores = set()
    cursor = temp_db.cursor()
    data = cursor.first()
    while data:
        temp_value = float(data[0].decode("utf-8"))
        _id = data[1] if data[1].isdigit() else None
        #checks the condition which is a string that was cleaned earlier and passed as a tuple
        if condition == ">":
            if temp_value > value:
                scores.add(_id)
        elif condition == "<":
            if temp_value < value:
                scores.add(_id)
        data = cursor.next()
    cursor.close()
    temp_db.close()
    return scores

#this handles checking if a stream already exists
#if a stream already exists then we must not create
#so this returns a stream or the tmp_set depending on if modified is True or False
def setCheck(stream, tmp_set, modified):
    return tmp_set if len(stream) == 0 and not modified else stream

#this combines setCheck and combine. makes code easier to read
def setcombine(stream, tmp_set, modified):
        stream = setCheck(stream, tmp_set, modified)
        stream = combine(stream, tmp_set)
        return stream

#This takes two sets and grabs intersecting values
#intersecting values are important because all conditions must be true
#returns a set of ids
def combine(stream, tmp_set):
    #stream is the current set
    #tmp_set is the new set that we will compare stream with
    #if values are in stream and tmp_set we will add it to a new set
    #named combined
    if stream is None and tmp_set:
        return tmp_set
    elif len(tmp_set) > 0  and len(stream) > 0:
        combined = set()
        for _id in tmp_set:
            if _id in stream:
                combined.add(_id)
        return combined
    else:
        return stream

#this handles all ppdate conditions. returns a set of results.
def dates(query):
    review_db = db.DB()
    review_db.open("rw.idx")
    cursor = review_db.cursor()
    data = cursor.first()
    date_asked = time.mktime(datetime.datetime.strptime(query[2], "%Y/%m/%d").timetuple())
    condition = query[1]
    results = set()
    while data:
        _id = data[0]
        #parsing the data in order to grab the date
        review_split = str(data[1]).split('",')
        review_split = review_split[2].split(',')
        date = float(review_split[2]) if len(review_split) > 2 else False
        if condition == ">" and date:
            if date > date_asked:
                results.add(_id)
        if condition == "<" and date:
            if date < date_asked:
                results.add(_id)
        data = cursor.next()
    cursor.close()
    review_db.close()
    return results

#handles all pprice conditions and returns a set of results
def price(query):
    review_db = db.DB()
    review_db.open("rw.idx")
    cursor = review_db.cursor()
    data = cursor.first()
    price_asked = float(query[2])
    condition = query[1]
    results = set()
    while data:
        #parsing the data in order to grab the price
        review_split = str(data).split('",')
        price = str(review_split[1]).split(',')[0]
        _id = data[0]
        price = float(price) if price != "unknown" else False
        if condition == ">" and price:
            if price > price_asked:
                results.add(_id)
        elif condition == "<" and price:
            if price < price_asked:
                results.add(_id)
        data = cursor.next()
    cursor.close()
    review_db.close()
    return results

#Takes a list of keys and prints them



def basic(fp, _id):
    tmp_db = db.DB()
    tmp_db.open(fp)
    result = tmp_db.get(_id)
    print("result", result)
    tmp_db.close()
    return result

def runr(fp, stream):
    review_db = db.DB()
    review_db.open(fp)
    reviews = {}
    count = 1
    sorted_set = sorted(stream)
    for _id in sorted_set:
        review = review_db.get(_id)
        _count_ = str(count)
        reviews[_count_] = review
    review_db.close()
    return reviews

def menu():
    os.system('clear')
    print("#################")
    print("BerkeleyDB Search")
    print("#################")
    print()

#this handles starting the app
def start():
    quit = False
    while not quit:
        menu()
        queries = input("> ")
        if queries:
            #grabs the query unparsed and passes it to search
            search(queries)
            choice = input("press any button to continue or q for quit ")
            if choice == "q":
                quit = True
        else:
            quit = False

start()
os.system('clear')
sys.exit()

