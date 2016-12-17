## script to resize image from a given folder
## films GIBOIRE 2016

import PIL
from PIL import Image
import glob
import os


for item in dir(PIL):
	print item

folderPath = "H:/WORK_PROJECTS/SPRAYFILMS/GIBOIRE/2D/AE/medias/BUSINESS/visuels_resize"


folderContent = glob.glob(folderPath+"\*")
basewidth = 1920

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