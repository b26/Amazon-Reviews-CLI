import bsddb
class BDB:
	db = None
	split_sign = ";;;"
	def __init__(self, name, mode, ss):
		self.db = bsddb.btopen(name, mode)
		self.split_sign = ss
	def get(self,key):
		if self.db.has_key(key) == True:
			val = self.db[key]
			return val.split(self.split_sign)
		else:
			return []
	def insert(self,key, value):
		val = ""
		if self.db.has_key(key) == True:
			val = self.db[key]
		val += self.split_sign + value
		self.db[key] = val

####################
x = BDB('fc.db','c',";;;")
x.insert('1','Student')
x.insert('1','James')
x.insert('1','Dot')
y = x.get('1')
print(y)
