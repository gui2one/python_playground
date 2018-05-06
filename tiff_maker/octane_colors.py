from PIL import Image
import numpy as np
import math

DIM = 4096
width = DIM
height = DIM
totalColors = math.pow(256,3.0)

array = np.zeros(( width, height,3), dtype=np.uint8)

# for x in range(DIM):
#     for y in range(DIM):
#         index =  x + ( DIM * y)
#         array[x, y, 0] = index  / 256
#         # print (array2[x, y])
#         pass

for r in range(256):
    for g in range(256):
        for b in range(256):
            index = r + (g * 256) + ( b * 256 * 256)

            x_coord = int(index % DIM)
            y_coord = int(index / DIM)
            array[x_coord, y_coord] = [r ,g,b]
img = Image.fromarray(array)
img.save("test.tiff")

print (totalColors , math.sqrt(totalColors))

print (array)