

text = u'''g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj.'''


codeString = []



for char in text :

	if ord(char) >=97 and ord(char)< 121 :
		codeString.append(chr(ord(char)+2 -32))
	else :

		index = ord(char)
		codeString.append( chr(index) )
		print ord(char),"1111111111",index
	

print ''.join(str(codeString))
print str(codeString)

# for i in range(32,125):
# 	print i, '--->', chr(i)