import codecs
import os
import io

import pysrt
rootDir = "C:/users/gui2one/downloads"
allFiles = os.listdir(rootDir)


srtFiles = []
for fileName in allFiles:
	fullPath = rootDir + "/"+ fileName
	if not os.path.isdir(fullPath):
		name, ext = os.path.splitext(fullPath )
		if ext == ".srt":
			srtFiles.append(fullPath)

print len(srtFiles)

for file in srtFiles:
	subs = pysrt.open(file)
	print subs[0].text


