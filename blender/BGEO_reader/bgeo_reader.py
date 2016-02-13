import struct

f = open('F:/HOUDINI_15_playground/geo/simple_grid.bgeo','rb')

header = struct.unpack('9c', f.read(9)) ## PGEOMETRY

print header