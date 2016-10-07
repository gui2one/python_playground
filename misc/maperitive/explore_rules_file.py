
import re
import struct
rgbstr='222222'
rgb = struct.unpack('BBB',rgbstr.decode('hex'))

print rgb

print ('%02x%02x%02x'%(rgb[0], rgb[1], rgb[2]))

f = open("F:/Maperitive/Rules/Default.mrules","r")

lines = f.readlines()

f.close()

for i,line in enumerate(lines):
	if line.find("#") != -1:

		
		
		rgbstr = line.split("#")[1][:6]
		

		
		rgb = struct.unpack('BBB',rgbstr.decode('hex'))
		# print re.split('; |, ',_str)[0]

		print 'line ',i, '-->', rgbstr, rgb