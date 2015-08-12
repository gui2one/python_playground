import sys
import time

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

sys.stdout.write('some data')
sys.stdout.flush()
time.sleep(2) # wait 2 seconds...
restart_line()
sys.stdout.write('other different data')
sys.stdout.flush()