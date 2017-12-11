import ftplib
import urllib2

import json
# for item in dir(urllib):
# 	print item


response = urllib2.urlopen("https://api.wheretheiss.at/v1/satellites/25544")

jsonData = json.loads(response.read())

print jsonData["altitude"]

passwd_file = open('F:/000_ISS_position/New Text Document.txt',"r")
passwd = passwd_file.read()
ftp = ftplib.FTP("sprayfilm.fr")
ftp.login("sprayfilm",passwd)
ftp.cwd("/httpdocs/gui2one/test1")

# for item in dir(ftp):
# 	print item

local_file = "iss_coords.txt"
ftp.cwd("python")
ftp.storlines('STOR '+local_file,open(local_file,"r"))

# local_file.close()

# ftp.dir()

# ftp.close()
