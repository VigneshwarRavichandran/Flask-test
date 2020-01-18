from flask_mysqldb import MySQL
import MySQLdb

class Db:
	def __init__(self):
		self.connection = MySQLdb.connect(host="localhost", user = "root", passwd = "123456", db = "doodleblue")
		
	def name_exists(self, name):
		cursor = self.connection.cursor()
		cursor.execute("select name from eg1 where name=(%s)",[name])
		value = cursor.fetchall()
		#this if condition to check name already is taken or not
		if len(value) != 0:
			return True
		return False