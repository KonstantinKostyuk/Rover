# ACTUAL
import sys
from PySide.QtCore import *
from PySide.QtGui import *
import serial
import pygame
import time
import subprocess
from pygame.locals import *

class Form(QDialog):

    text = ""
    cmd = ""
    M1Speed = 0
    M2Speed = 0
    Claw = 0

    def __init__(self, parent = None):
        super(Form, self).__init__(parent)

        self.browser = QTextBrowser()

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.setWindowTitle("Control by release")

        pygame.init()
        self.xbox = pygame.joystick.Joystick(0).init()


    def read_xbox(self):
        DRIVE_DEATHZONE = 0.2
        RATIO = (8 - 2) / (1 - DRIVE_DEATHZONE)
        RATIO2 = (6 - 2) / (1 - DRIVE_DEATHZONE)
        LATENCY = 0.01
        self.drive_package = 1100
        self.speed_mode_com = 0
        self.steer_mode_com = 0
        self.drive_com = 0
        self.steer_com = 0
        self.steer_flag = False
        self.drive_flag = False
        self.old_time = time.clock()
        while 1:
            for event in pygame.event.get():
                self.first_time = False
                if event.type == JOYBUTTONDOWN:
                    if event.button == 0: #Forward
                        self.M1Speed = self.M1Speed + 100
                        self.M2Speed = self.M2Speed + 100
                    if event.button == 1: #Stop
                        self.M1Speed = 0
                        self.M2Speed = 0
                    if event.button == 2: #Back
                        self.M1Speed = self.M1Speed - 100
                        self.M2Speed = self.M2Speed - 100
                    if event.button == 4: #L Fast
                        self.M1Speed = self.M1Speed + 500
                    if event.button == 6: #L
                        self.M1Speed = self.M1Speed + 100
                    if event.button == 5: #R Fast
                        self.M2Speed = self.M2Speed + 500
                    if event.button == 7: #R
                        self.M2Speed = self.M2Speed + 100
                    if event.button == 8: #Cat
                        self.Claw = 1
                    if event.button == 9: #Rel
                        self.Claw = 0
                    cmd = str(self.M1Speed) + ":" + str(self.M2Speed) + ":" + str(self.Claw)
#                    subprocess.call(["plink.exe", "-ssh", "ubuntu@192.168.0.101", "-pw", "ubuntu", "echo", cmd, ">", "cmd.txt"])
#                    subprocess.call(["python", "sender.py", cmd ])
                    self.text = str(event.button) + ":" + cmd
                    self.updateUi()				

    def keyReleaseEvent(self, e):
        print(e.key())
        if e.key() > 57:
            self.offset = 32
        else:
            self.offset = 0
        self.text = chr(e.key() + self.offset)
        self.updateUi()

    def updateUi(self):
        try:
            self.browser.append("%s" % self.text)
#			send-comand by ssh
        except:
            self.browser.append(("<font color = red>%s is invalid</font>" % self.text))

app = QApplication(sys.argv)
form = Form()
form.show()
form.read_xbox()
app.exec_()