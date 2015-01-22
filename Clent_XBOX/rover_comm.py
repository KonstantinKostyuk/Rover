# ACTUAL
# import sys
# import serial
# import pygame
# import time
# from pygame.locals import *
import subprocess

def send2rover(speed_l, speed_r, claw):
	print('Sended:', speed_l ,speed_r, claw)
	cmd = str(speed_l) + ":" + str(speed_r) + ":" + str(claw)
	subprocess.call(["python", "sender.py", cmd ])