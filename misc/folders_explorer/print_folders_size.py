### print folders size
import os
import glob
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


# print get_size("F:\\openEXR")
items = glob.glob("C:/Program Files/*")

for item in items:
	print item, " ---> ", get_size(item)