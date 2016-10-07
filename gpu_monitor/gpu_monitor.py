import msvcrt # built-in module
import curses
from pynvml import *
from time import sleep
import math

def clearScreen(screen):
	dims = screen.getmaxyx()
	for i in range(dims[0]-1):
		
		screen.addstr(i,0," "*dims[1], curses.color_pair(1))


def kbfunc(): 
   x = msvcrt.kbhit()
   if x: 
      ret = ord(msvcrt.getch()) 
   else: 
      ret = 0 
   return ret

def drawBar(screen,y,ratio):
	width = screen.getmaxyx()[1]
	numBlocks = int((ratio)*(width-1))
	screen.addstr(y,0, " "*numBlocks, curses.color_pair(2))
	screen.addstr(y,numBlocks, " "*(width - numBlocks), curses.color_pair(3))


nvmlInit()
deviceCount = nvmlDeviceGetCount()

handle = nvmlDeviceGetHandleByIndex(0)



screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN)


num = 0
done = False


while not done:
	memInfo = nvmlDeviceGetMemoryInfo(handle)
	utilization = nvmlDeviceGetUtilizationRates(handle)

	clearScreen(screen)

	
	
	
	screen.addstr(0,0,"   Gpu : %s" % nvmlDeviceGetName(handle), curses.color_pair(1))

	
	screen.addstr(2,3,"Usage : %s %%" % utilization.gpu, curses.color_pair(1))
	drawBar(screen, 3, float(utilization.gpu) / 100.0)

	screen.addstr(4, 3, "Temperature : %s degrees C" % (int(nvmlDeviceGetTemperature(handle,0))), curses.color_pair(1))
	screen.addstr(5,3,"Memory :", curses.color_pair(1))
	screen.addstr(6,3,"Total: %s -- Used : %s -- Free: %s " % (memInfo.total/1024/1024, memInfo.used/1024/1024, memInfo.free/1024/1024), curses.color_pair(1))
	

	drawBar(screen, 7, (float(memInfo.used) / memInfo.total))
	

	screen.refresh()

	#print num
	#num += 1

	if msvcrt.kbhit():
		c = msvcrt.getch()
		if c == "q":
			print "you pressed",c,"so now i will quit"
			done = True



	sleep(0.5)

screen.endwin()

