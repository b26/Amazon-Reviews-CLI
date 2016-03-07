from bsddb3 import db
# Davood's file
# Updated by Kriti
# Command to run: python b_bsddb3.py
class BDB:
	database = None
	split_sign = ";"
	def __init__(self, name):
		self.database = db.DB()
		#self.database.set_flags(db.DB_DUP)
		self.database.open(name, None, db.DB_BTREE, db.DB_CREATE)

	def get(self,key):
		if self.database.has_key(key) == True:
			val = self.database[key]
			in_str = str(val,'ascii')
			#print(in_str)
			return in_str.split(self.split_sign)
		else:
			return  []

	def insert(self,key, value):
		if self.database.has_key(key)== False:
			self.database[key] = value
		else:
			val = str(self.database[key],'ascii')
			self.database[key] = val + self.split_sign + value
			

####################
DATABASE = 'f112.db'
x = BDB(DATABASE)
x.insert(b'1',"apple")
x.insert(b'1',"pear")
x.insert(b'1',"grapes")
y = x.get(b'1')
print(y)
