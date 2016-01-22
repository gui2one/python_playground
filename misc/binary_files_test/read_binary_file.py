import struct


fileName = 'binary_filetest.g21'

### read data back

rFile = open(fileName,'rb')
headerStruct = struct.Struct('L I')
headerData = rFile.read(8)

header = headerStruct.unpack(headerData)
numPoints = header[0]
numAttr = header[1]



attrStruct = struct.Struct('d d d')

for i in range(numPoints):
	data = rFile.read(24)
	print(attrStruct.unpack(data))
rFile.close()



## x	pad byte	no value	 	 
## c	char	string of length 1	1	 
## b	signed char	integer	1	(3)
## B	unsigned char	integer	1	(3)
## ?	_Bool	bool	1	(1)
## h	short	integer	2	(3)
## H	unsigned short	integer	2	(3)
## i	int	integer	4	(3)
## I	unsigned int	integer	4	(3)
## l	long	integer	4	(3)
## L	unsigned long	integer	4	(3)
## q	long long	integer	8	(2), (3)
## Q	unsigned long long	integer	8	(2), (3)
## f	float	float	4	(4)
## d	double	float	8	(4)
## s	char[]	string	 	 
## p	char[]	string	 	 
## P	void *	integer	 	(5), (3)