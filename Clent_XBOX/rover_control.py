# ACTUAL
import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *
from rover_comm import *
import pygame
import subprocess
from pygame.locals import *
# import time
# import serial

class Form(QDialog):

    text = ""

    def __init__(self, parent = None):
        super(Form, self).__init__(parent)
        # layout = QVBoxLayout()
        layout = QGridLayout()
        layout.setSpacing(10)

        self.label_title = QLabel('<b>Rover</b>')
        font1 = self.label_title.font()
        font1.setPointSize(20)
        font2 = self.label_title.font()
        font2.setPointSize(16)
        font3 = self.label_title.font()
        font3.setPointSize(12)
        self.label_title.setFont(font1)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label1 = QLabel('Control Scheme')
        self.label1.setFont(font2)
        self.label2 = QLabel('Speed Mode')
        self.label2.setFont(font2)
        self.label3 = QLabel('Comands')
        self.label3.setFont(font3)
        self.label4 = QLabel('Speeds')
        self.label4.setFont(font3)
        self.browser1 = QTextBrowser()
        self.browser2 = QTextBrowser()

        layout.addWidget(self.label_title, 0, 0, 1, 2)
        layout.addWidget(self.label1, 1, 0)
        layout.addWidget(self.label2, 2, 0, 1, 2)
        layout.addWidget(self.label3, 3, 0)
        layout.addWidget(self.label4, 3, 1)
        layout.addWidget(self.browser1, 4, 0)
        layout.addWidget(self.browser2, 4, 1)
        self.setLayout(layout)
        self.setWindowTitle("Rover Control")
        # self.ser = serial.Serial('COM8', 9600, timeout = 0.2)
        # self.ser.setRTS(0)
        pygame.init()
        self.xbox = pygame.joystick.Joystick(0).init()

    def send_comm(self, speed_l, speed_r, claw):
        if (speed_l != self.speed_l_old) or (speed_r != self.speed_r_old) or (claw != self.claw_old):
            cur_time = time.time()
            if cur_time - self.time_old >= self.TIME_LATENCY:
                send2rover(speed_l, speed_r, claw)
                self.time_old = cur_time
                self.updateUi()
                self.speed_l_old = speed_l
                self.speed_r_old = speed_r
                self.claw_old = claw
	
    def remap(self, OldValue, OldMin, OldMax, NewMin, NewMax):
    # Mashtab function
        OldRange = (OldMax - OldMin)
        NewRange = (NewMax - NewMin)
        NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        return NewValue

    def clamp(self, n, minn, maxn):
    # Diapazon Function
        if n < minn:
            return minn
        elif n > maxn:
            return maxn
        else:
            return n

    def sign(self, val):
        if val < 0: return -1
        else: return 1

    def read_xbox(self):
        MIN_SPEED = 500 # 
        MAX_SPEED = 1500 # 
        SLOW_RATIO = 0.5 # 
        # Left XBOX
        X1_AXIS = 0
        Y1_AXIS = 1
        # Rigt XBOX
        X2_AXIS = 4
        Y2_AXIS = 3
        # Dead zone
        Y_DZONE = 0.2
        X_DZONE = 0.2
        # Buttons XBOX
        X_BUTTON = 2 # 
        Y_BUTTON = 3 # 
        B_BUTTON = 1 # 
        A_BUTTON = 0 # 
        STOP_BUTTON = 5
        self.TIME_LATENCY = 0.0

        control_scheme = 1
        slow_mode = False # 
        max_speed = MAX_SPEED
        speed = 0
        speed_l = 0
        speed_r = 0
        steer = 0
        claw = 0 #
        self.speed_l_old = 0
        self.speed_r_old = 0
        self.claw_old = 0
        self.time_old = 0

        self.updateLabel(control_scheme, slow_mode)
        while 1:
            for event in pygame.event.get():
                if event.type == JOYBUTTONDOWN:
                    self.browser1.append(str(event.button))
                    if event.button == X_BUTTON:
                        control_scheme = 1
                        self.browser1.append('Scheme 1')
                    if event.button == Y_BUTTON:
                        control_scheme = 2
                        self.browser1.append('Scheme 2')
                    # On/Off
                    if event.button == B_BUTTON:
                        slow_mode = not slow_mode
                        if slow_mode:
                            max_speed = MAX_SPEED * SLOW_RATIO
                            self.browser1.append('Slow Mode')
                        else:
                            max_speed = MAX_SPEED
                            self.browser1.append('Normal Mode')
                    # 
                    if event.button == A_BUTTON:
                        if claw == 0: claw = 1
                        else: claw = 0
                        self.browser1.append('Catche')
                    self.updateLabel(control_scheme, slow_mode)
                    # Send to rover
                    self.send_comm(speed_l, speed_r, claw)
					
                    if event.button == STOP_BUTTON:
                        speed_l = 0
                        speed_r = 0
                        self.browser1.append('STOP')
                        self.send_comm(speed_l, speed_r, claw)
						

                if event.type == JOYAXISMOTION:
                    # Scheme 1
                    if control_scheme == 1:
                        # Forward
                        if event.axis == Y1_AXIS:
                            if abs(event.value) > Y_DZONE:
                                speed = -self.sign(event.value)*self.remap(abs(event.value), Y_DZONE, 1, MIN_SPEED, max_speed)
                            else: speed = 0
                        # Turns
                        if event.axis == X1_AXIS:
                            if abs(event.value) > X_DZONE: steer = event.value
                            else: steer = 0
                        speed_r = speed*(1 + steer)
                        speed_l = speed*(1 - steer)
                        # Speed Limit
                        speed_l = self.clamp(speed_l, -MAX_SPEED, MAX_SPEED)
                        speed_r = self.clamp(speed_r, -MAX_SPEED, MAX_SPEED)
                        # Rover rotation
                        if event.axis == X2_AXIS:
                            if abs(event.value) > Y_DZONE:
                                speed_l =  -self.sign(event.value)*self.remap(abs(event.value), Y_DZONE, 1, MIN_SPEED, max_speed)
                                speed_r =  self.sign(event.value)*self.remap(abs(event.value), Y_DZONE, 1, MIN_SPEED, max_speed)

                    # Scheme 2
                    if control_scheme == 2:
                        # Left track
                        if event.axis == Y1_AXIS:
                            if abs(event.value) > Y_DZONE:
                                speed_l = -self.sign(event.value)*self.remap(abs(event.value), Y_DZONE, 1, MIN_SPEED, max_speed)
                            else: speed_l = 0
                        # Right track
                        if event.axis == Y2_AXIS:
                            if abs(event.value) > Y_DZONE:
                                speed_r = -self.sign(event.value)*self.remap(abs(event.value), Y_DZONE, 1, MIN_SPEED, max_speed)
                            else: speed_r = 0
                    speed_l = int(speed_l)
                    speed_r = int(speed_r)
                    self.text = str(speed_l) + '  ' + str(speed_r)
                    # print(speed_l, speed_r, claw)
                    # self.updateUi()
                    # Send to Rover
                    self.send_comm(speed_l, speed_r, claw)



    def updateUi(self):
        try:
            self.browser2.append("%s" % self.text)
            # self.ser.write(self.text.encode("utf-8"))
        except:
            self.browser2.append(("<font color = red>%s is invalid</font>" % self.text))

    def updateLabel(self, control_scheme, slow_mode):
        self.label1.setText('Scheme ' + str(control_scheme))
        speed_mode_text = 'Speed Mode: '
        speed_mode_text_add = 'Normal'
        if slow_mode: speed_mode_text_add = 'Slow'
        self.label2.setText(speed_mode_text + speed_mode_text_add)


app = QApplication(sys.argv)
form = Form()
form.show()
form.read_xbox()
app.exec_()