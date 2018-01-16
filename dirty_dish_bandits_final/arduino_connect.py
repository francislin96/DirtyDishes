import serial
a
ser1=serial.Serial('COM3',9600, timeout=None)
x = ser1.write(b'5')


try:
	arduino = serial.Serial('COM3', 9600, timeout=None)
except:
	print('Please check the port')


while True:
	#x = str(arduino.readline())
	#x = x[2:]
	#x = x[:-8]

	#if x != "b''":
	print(x)
