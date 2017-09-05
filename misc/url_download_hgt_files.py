import os
from urllib import request
from bs4 import BeautifulSoup


rootDir = os.path.dirname(os.path.abspath(__file__))
# print(os.path.join(rootDir, 'hgt_files'))

# from BeautifulSoup import BeautifulSoup
url = 'https://dds.cr.usgs.gov/srtm/version1/Eurasia'

response = request.urlopen(url)

soup = BeautifulSoup(response,'html.parser')

# print(soup)

links = soup.find_all('a')

for i,link in enumerate(links):
    if i != 0:    
        fileName = link.get('href')
        fileURL = os.path.join(url, fileName).replace("\\","/")

        print(fileURL,"-----------------")
        newFilePath = os.path.join(rootDir, "hgt_files", fileName)
        with open(newFilePath,"wb")  as f:
            f.write( request.urlopen(fileURL).read())
            # f.write("hello")




