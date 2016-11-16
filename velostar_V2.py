import urllib2

data = urllib2.urlopen("www.google.com")
data.close()
print data