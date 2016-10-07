import sqlite3

conn = sqlite3.connect('cities.db')

cursor = conn.cursor()

# cursor.execute("""SELECT * FROM cities WHERE population>=3000000""")
cursor.execute("""SELECT * FROM cities WHERE population=0""")
response = cursor.fetchall()	
conn.close()


print len(response)
for i,entry in enumerate(response):
	if i < 500:
		print entry