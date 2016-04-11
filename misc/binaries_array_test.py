import array
import sys

# Create an array of 16-bit signed integers
a = array.array("H", range(10))
# Write to file in big endian order
if sys.byteorder == "little":
    a.byteswap()
with open("data", "wb") as f:
    a.tofile(f)
# Read from file again
b = array.array("h")
with open("data", "rb") as f:
    b.fromfile(f, 10)
if sys.byteorder == "little":
    b.byteswap()