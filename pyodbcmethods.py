#connect to the SQL database with username and password. Returns a cursor object to direct future SQL methods.
#update the variables below if needed
def connect():
	import pyodbc
	server = '<REPLACE>' #SQL server name
	database = '<REPLACE>' #SQL server database
	username = '<REPLACE>' #SQL server user ID
	password = '<REPLACE>' #SQL server password
	driver = 'ODBC Driver 13 for SQL Server' #this computer's driver for SQL server. Can be 'ODBC Driver # for SQL Server' or 'SQL Server Native Client #'
	
	cnxn = pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor() #logs in, creates a target for SQL queries called in methods after this
	return cursor
