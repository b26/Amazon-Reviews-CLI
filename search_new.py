from bsddb3 import db
import os
import sys
import datetime
import time
review_db = db.DB()
review_db.open("rw.idx")
review_cur = review_db.cursor()
idSet = set()
# IMPORTANT!! We may be given queries in the format rdate>2001/01/23 rscore<3 and pprice>60, we cannot depend on their being spaces between the >< symbols and the numbers/command!
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
	#search is given a string and idSet. It splits the string presumnably
    string = string.split()
    queries = []
	#question 7 isn't working right, it needs to actually read the first word, but it's just skipping it right now. I don't know how to change that without breaking everything.
    # if len(string) > 1:
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
    #print(idSet)
# These handle 8, 9, and 10
#FIXME you mentioned to build a loop, but you wrote code outside the loop.
if string[1] == "rdate" and len(string) > 6:
    	cost = runr(idSet)
    	priceCheck(cost, string, 10)
    	dateCheck(cost, string)
    elif string[0] == "pprice":
    	cost = runr(idSet)
    	priceCheck(cost, string, 0)
    elif string[1] == "rdate":
    	date = runr(idSet)
    	dateCheck(date, string)

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
# find is only run for rscore questions. Needs to be more generalized.
def find(fp, string):
	#condition is set to the second piece of the split string
    if string[0] == "rscore":
    	condition = string[1]
    	value = float(string[2])
    else:
    	condition = string[2]
    	value = float(string[3])
    temp_db = db.DB()
    temp_db.open(fp)
    cursor = temp_db.cursor()
    data = cursor.first()
#temporary database that is a copy of the actual database is scanned.
    while data:
        temp_value = float(data[0].decode("utf-8"))
        if condition == ">":
            if temp_value > value:
                print(data)
        elif condition == "<":
            if temp_value < value:
                print(data)
        data = cursor.next()
    cursor.close()
    temp_db.close()
#temp database is closed, back to search.

def runr(idSet):
    reviews_list = []
    for _id in idSet:
        review = review_db.get(_id)
        reviews_list.append(review)
    return reviews_list
#mostly just added in the whole comparison part. Unknown values are ignored, as are all products with a price of 0. Hopefully that won't come up.
def priceCheck(review_list, string, ten):
	if ten == 0:
		condition = string[1]
		value = float(string[2])
		for review in review_list:
			review = str(review).split('",')
			price = str(review[1]).split(',')[0]
			if price == "unknown":
				price = 0
			pvalue = float(price)
			if condition == ">":
				if pvalue > value and pvalue > 0:
					print("price", price)
			elif condition == "<":
				if pvalue < value and pvalue > 0:
					print("price", price)
	if ten == 10:
		value1 = float(string[6])
		value2 = float(string[9])
		for review in review_list:
			review = str(review).split('",')
			price = str(review[1]).split(',')[0]
			pvalue = float(price)
			if pvalue > value1 and pvalue < value2:
				print("price", price)
#set this up, converts the value from string into a datetime, grabs the datetime from the file using the same technique as priceCheck
#then compares them in the same way
def dateCheck(review_list, string):
	value = time.mktime(datetime.datetime.strptime(string[3], "%Y/%m/%d").timetuple())
	condition = string[2]
	for review in review_list:
		review = str(review).split('",')
		date = str(review[2]).split(',')[2]
		pvalue = float(date)
		if condition == ">":
			if pvalue > value:
				print("date", date)
		elif condition == "<":
			if pvalue < value:
				print("date", date)


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
	##runs search, what is idSet?
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

