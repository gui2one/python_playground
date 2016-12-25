# -*- coding: utf-8 -*-
## script to resize image from a given folder
## films GIBOIRE 2016

import PIL
from PIL import Image
import glob
import os


for item in dir(PIL):
	print item

folderPath = u"D:/WORK/SPRAYFILM/GIBOIRE/PIECES_FOURNIES/retour_FINAL/Moyens -- Esprit d'équipe -- esprit sportif/resize"


print "folderPath : ", folderPath
# return 0


folderContent = glob.glob(folderPath+"//*")
basewidth = 1920

print folderContent
for i,imgFile in enumerate(folderContent):

	img = Image.open(imgFile)

	fileName, fileExt = os.path.splitext(imgFile)
	print i, '-->',fileName
	if(img.size[0] > basewidth):
		
		try:
			wpercent = (basewidth / float(img.size[0]))
			hsize = int((float(img.size[1]) * float(wpercent)))
			img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
			
		except IOError: 
			print "IOERROR", "-->", imgFile

	img.save(fileName+'.jpg',"JPEG")