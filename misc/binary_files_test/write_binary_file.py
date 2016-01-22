
import struct


dataIn = ''

### HEADER
numPoints = 500
numAttr = 3
header = (numPoints, numAttr)
headerStruct = struct.Struct('L I')
dataIn += headerStruct.pack(*header)

#### HEADER end

for i in range(0,100000):
	values = (i*0.2,i*0.33,i*0555)

	### create struct format
	s = struct.Struct('d d d')

	### pack data
	packedData = s.pack(*values)

	dataIn += packedData


fileName = 'binary_filetest.g21'
f = open(fileName,'wb')

f.write(dataIn)

f.close()





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