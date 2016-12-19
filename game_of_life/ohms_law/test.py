

import pygame
import os, sys

sys.path.insert(0, os.path.abspath("../modules"))
from gui2oneUI import *
import gui2one_utils as g2


print g2.resistance(0.02,12-(1.7*4))
width, height = 400, 400
os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((width, height))
pygame.init()

ui = gui2oneUI(screen)

margin = 10
uiX = margin
uiY = margin

voltageField = EditText(screen,uiX,uiY ,100, 30, "Voltage",12)
ui.addItem(voltageField)

uiY += 40
ledVoltageField = EditText(screen,uiX,uiY ,100, 30, "LED Voltage (single)",1.7)
ui.addItem(ledVoltageField)

uiY += 40
desiredCurrentField = EditText(screen,uiX,uiY ,100, 30, "Desired Current in single LED (in Amps)",0.02)
ui.addItem(desiredCurrentField)

uiY += 40
numLedsField = EditText(screen,uiX,uiY ,100, 30, "Number of LEDs",1)
ui.addItem(numLedsField)

voltage = voltageField.value
ledVoltage = ledVoltageField.value
desiredCurrent = desiredCurrentField.value
numLeds = numLedsField.value


def cb():

	val = g2.resistance(desiredCurrent, voltage-( ledVoltage * numLeds ))
	resultField.text = str(val)

uiY += 40
btn1 = Button(screen,  uiX,uiY,100,30,"Calculate")
btn1.subscribe(cb)
ui.addItem(btn1)

uiY += 50
line1 = Line(screen, uiX, uiY, 200,10)
ui.addItem(line1)

uiY += 30
resultField =  StaticText(screen,uiX,uiY ,100, 30, "Result","Result")
ui.addItem(resultField)


class Core(object):
	def __init__(self, surface, name):
		pygame.display.set_caption(name)
		self.screen = surface

	def dispatch(self, event):
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			sys.exit()     
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pass

	def run(self):
		global voltage
		global ledVoltage
		global desiredCurrent
		global numLeds
		# global resultField

		while True:
			# print voltage
			voltage = float(voltageField.value)
			ledVoltage = float(ledVoltageField.value)
			desiredCurrent = float(desiredCurrentField.value)
			numLeds = float(numLedsField.value)



			
			# print voltage
			self.screen.fill([50,50,50])			
			ui.draw()
			ui.eventUpdate()

			# for event in pygame.event.get():
			# 	self.dispatch(event)



			pygame.display.flip()

if __name__ == '__main__':
	main = Core(screen, 'Node')
	main.run()