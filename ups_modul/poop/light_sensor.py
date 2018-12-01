#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 7

def rc_time (pin_to_circuit):
	count = 0

	#Output on the pin for 
	GPIO.setup(pin_to_circuit, GPIO.OUT)
	GPIO.output(pin_to_circuit, GPIO.LOW)
	time.sleep(0.1)

	#Change the pin back to input
	GPIO.setup(pin_to_circuit, GPIO.IN)

	#Count until the pin goes high
	if (GPIO.input(pin_to_circuit) == GPIO.LOW):
		count += 1

	return count


def poop_zapis_on(time_on):
	with open(poop_log, "a") as fp:
		fp.write("POOP ON {}\n".format(time.strftime(time_format, time.localtime(time_on))))


def poop_zapis_off(time_off):
	with open(poop_log, "a") as fp:
		fp.write("POOP OFF {}\n".format(time.strftime(time_format, time.localtime(time_off))))	  


def poop_timer(time_on):
	t2 = time.time()
	t_delta = t2 - time_on
	print("kadil jsi {0:.2f}s".format(t_delta))
	time.sleep(0.01)
	return t2


time_format = "%d.%m.%Y %H:%M:%S"
poop_log = "poop_log.txt"


#Catch when script is interupted, cleanup correctly
try:
	poop_status = 0
	# Main loop
	while True:
		time.sleep(0.5)
		light_status = rc_time(pin_to_circuit)
		if light_status == 1 and poop_status == 0:
			t1 = time.time()
			poop_zapis_on(t1)
			poop_status = 1
		elif light_status == 0 and poop_status == 1:
			t2 = poop_timer(t1)
			poop_zapis_off(t2)
			poop_status = 0
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()
