## script to check image color Mode
## films GIBOIRE 2016

import PIL
from PIL import Image
import glob
import os


for item in dir(PIL):
	print item

folderPath = "H:\WORK_PROJECTS\SPRAYFILMS\GIBOIRE\PIECES_FOURNIES\FILM_promotion\partie_2"


folderContent = glob.glob(folderPath+"\*")
basewidth = 1920

for i,imgFile in enumerate(folderContent):
	fileName, fileExt = os.path.splitext(imgFile)

	goodExt = [".jpg", ".JPG",".jpeg", ".JPEG",".TIFF",".tiff",".TIF",".tif",".PNG",".png",".GIF",".gif"]
	
	if not os.path.isdir(fileName) and fileExt in goodExt:
	
		img = Image.open(imgFile)

		
		print i, '-->',img.mode, "EXT -->", fileName.split("\\")[-1:]
		if(img.size[0] > basewidth):
			
			try:
				wpercent = (basewidth / float(img.size[0]))
				hsize = int((float(img.size[1]) * float(wpercent)))
				img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
				
			except IOError: 
				print "IOERROR", "-->", imgFile

		img.convert('RGB').save(fileName+'_converted.jpg','JPEG')