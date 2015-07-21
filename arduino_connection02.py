import serial

ser = serial.Serial('COM3',9600)
while True:
	val = ser.readline()
	hou.node("/obj/geo1").parm('tx').set(float(val)*0.005)
	#print val