#! /usr/bin/env python
#-*- coding: utf-8 -*-





import sqlite3

f = open("worldcitiespop_____.txt",'r')

data = f.readlines()




f.close()

print data[0]

cities = []

for i,line in enumerate(data):
	if i != 0:
		dataArray = line.strip().split(',')	
		dataDict = {'country':dataArray[0], 'city':dataArray[1], 'accentCity':dataArray[2], 'region':dataArray[3], 'population':dataArray[4], 'latitude':dataArray[5], 'longitude':dataArray[6] }
		pop = dataDict['population']
		if pop == '':
			pop = 0

		if pop > 0:
			cities.append(dataDict)
print len(cities)



dbName = 'countries.db'
conn = sqlite3.connect(dbName)

conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
 ###delete table 'cities'
cursor = conn.cursor()
cursor.execute("""
DROP TABLE cities_subset
""")
conn.commit()
####################



#Country,City,AccentCity,Region,Population,Latitude,Longitude

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS cities_subset(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     country TEXT NOT NULL,
     city TEXT NOT NULL,
     accentCity TEXT NOT NULL,
     region TEXT NOT NULL,
     population INTEGER NOT NULL,
     latitude FLOAT NOT NULL,
     longitude FLOAT NOT NULL
)
""")
conn.commit()



cursor.executemany("""
INSERT INTO cities_subset(country, city, accentCity, region, population, latitude, longitude) VALUES(:country, :city, :accentCity, :region, :population, :latitude, :longitude)""", cities)

conn.commit()

conn.close()
