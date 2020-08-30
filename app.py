import sqlite3
import os
from prettytable import PrettyTable


CWD = os.getcwd()

def raiseException(customMsg):
	print(customMsg)

def connect_to_db(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		conn.row_factory = 	sqlite3.Row
	except Exception:
		raiseException("Connection Issue")
	return conn


def table_exists(conn,tblName):
	c = conn.cursor()
	c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?",[tblName])
	if c.fetchone()[0] != 1:
		return False
	return True

def getColumns(conn,tblName):
	if table_exists(conn,tblName):
		c = conn.cursor()
		c.execute("SELECT * from {}".format(tblName))
		records = c.fetchone()
		return [col[0] for col in c.description]
	else:
		return None

def create_record(conn,tblName='member',dataDict={}):
	'''
		Create tuple for any particular tables 
	'''
	if dataDict:
		cols = ",".join(col for col in dataDict.keys())
		fields = ','.join("?" for _ in range(len(dataDict.keys())))
		sqlQuery = "INSERT INTO "+ tblName +"(" + cols + ") VALUES (" + fields + ") "
		cursor = conn.cursor()
		try:
			cursor.execute(sqlQuery,list(dataDict.values()))
		except Exception as e:
			print(e)
			raiseException("Insertion failed")
		else:
			conn.commit()
			print("Insertion happened sucessfull ...")


	else:
		print("Please pass required data for {}".format(tblName))

def delete_record(conn,tblName='member',condDict={}):
	'''
		Delete any particular record from the tables based on some condition  
	'''
	if condDict:
		condition = " AND ".join(str(key+'='+ "'" + condDict[key] + "'") for key in condDict.keys())
		sqlQuery = "DELETE from {} where ".format(tblName) + condition
		try:
			conn.execute(sqlQuery)
		except Exception as e:
			print(e)
		else:
			conn.commit()
			print("Deletion happened sucessfully .. ")
	else:
		print("Please pass required condition to delete record from {}".format(tblName))

def update_record(conn,tblName='member',dataDict={},condDict={}):
	'''
		update columns based on some condition for a giver particular table 
	'''
	if condDict and dataDict:
		condition = " AND ".join(str(key+'='+ "'" + condDict[key] + "'") for key in condDict.keys())
		setString = " AND ".join(str(key+'='+ "'" + dataDict[key] + "'") for key in dataDict.keys())
		sqlQuery = "UPDATE " + tblName + " SET " + setString + " WHERE " + condition
		try:
			conn.execute(sqlQuery)
		except Exception as e:
			print(e)
		else:
			conn.commit()
			print("Updation happened sucussefully ... ")
	else:
		print("Please pass required data to do the update operation on {}".format(tblName))

def read_record(conn,tblName='member',colList=[]):
	'''
		To display records for any particular table 
	'''
	if not colList:
		sqlQuery = "SELECT * from {}".format(tblName)
	else:
		sqlQuery = "SELECT " + ','.join(colList) + " from {}".format(tblName)
	x = PrettyTable()
	cursor = conn.cursor()
	try:
		colList = getColumns(conn,tblName)
		x.field_names = colList
		cursor.execute(sqlQuery)
		if colList:
			rows = cursor.fetchall()
			for row in rows:
				x.add_row(row)
			print(x)
		else:
			print("No such table exists")
	except Exception as e:
		print(e)

def do_transaction(conn):
	'''
		All CRUD operation are happening here 
	'''
	loopCond = True
	while (loopCond):
		print("------------- E-Commerce Backend-----------")
		print("1. Create Record")
		print("2. Read Record")
		print("3. Update Record")
		print("4. Delete Record")
		print("5. Exit from the app")
		try:
			choice = int(input())
			if choice < 1 or choice > 5:
				print("Please choose value between 1-4 ")
			else:
				if choice == 5:
					loopCond = False
				else:
					tblName = input("Enter table name > ")
					colList = getColumns(conn,tblName)
					if choice == 1:
						if colList is not None:
							data = {}
							for col in colList:
								inp = input("Enter value for {} > ".format(col))
								data[col] = inp
							create_record(conn,tblName,data)
						else:
							print("Table does not exist ..")
					elif choice == 2:
						read_record(conn,tblName)
					elif choice == 3:
						print("Columns for this table :",colList)
						dataDict = {}
						condDict = {}
						print("Enter Set values for update .. ")
						while True:
							col,cond = input("Enter col and cond with ',' otherwise enter (-1,-1) : ").split(',')
							print(col,cond)
							if col == '-1' and cond == '-1':
								break
							dataDict[col] = cond
						print("Enter Condition for update .. ")
						while True:
							col,cond = input("Enter col and cond with ',' otherwise enter (-1,-1) : ").split(',')
							print(col,cond)
							if col == '-1' and cond == '-1':
								break
							condDict[col] = cond
						update_record(conn,tblName,dataDict,condDict)

					elif choice == 4:
						print("Columns for this table :",colList)
						condDict = {}
						while True:
							col,cond = input("Enter col and cond with ',' otherwise enter (-1,-1) : ").split(',')
							print(col,cond)
							if col == '-1' and cond == '-1':
								break
							condDict[col] = cond
						delete_record(conn,tblName,condDict)
		except Exception as e:
			print(e)

def runApp():
	'''
		connect to db
		do the transactions
		close the connection
	'''
	db_file = input("Enter the db file > ")
	db_filePath = os.path.join(os.getcwd(),db_file)
	conn = connect_to_db(db_filePath)
	if conn:
		conn.execute("PRAGMA foreign_keys = 1")	
		do_transaction(conn)
		conn.close()
	else:
		print("Connection to given db file failed ..")

#driver code
if __name__ == '__main__':
	runApp()