try:
    import RPi.GPIO as gpio
except ModuleNotFoundError:
    print("Could not import GPIO library! Exiting...")
    raise NoRPi
import time
from threading import Thread
import numpy as np
from RpiMotorLib import RpiMotorLib as rml


#Fill in with actual motor offsets
L0 = 0.5
L1 = 2

#MIN TIMES
SIGNAL_SETUP = 0.0000002
SIGNAL_HOLD = 0.0000002
STEP_HIGH = 0.000001
STEP_LOW = 0.000001


#PIN NUMBERS
#Change these to suit setup
M0_STEP = 26
M0_DIR = 27
M0_MSTEP = (6, 10, 11)

M1_STEP = 24
M1_DIR = 25
M1_MSTEP = (21, 22, 23)


class mountArm:
    def __init__(self):
        self.motors = [rml.A4988Nema(M0_DIR,M0_STEP,M0_MSTEP),rml.A4988Nema(M1_DIR,M1_STEP,M1_MSTEP)]
        self.theta = (0,0)
        self.mstep = "Full"
        self.stepdelay = .005
        self.mlock = False
        self.canReceive = False
    def _step2rad(self,mstep,steps):
        return steps*np.pi/100/mstep
    def _rad2step(self,mstep,theta):
        return 100/np.pi*mstep*theta
    def handleButtonPressedSignal(self, mccw):
        if !self.mlock:
            self.motors[mccw[0]].motor_go(!mccw[1], self.mstep)
            keepGoing = True
            while keepGoing:
                try:
                    self.theta[mccw[0]] += int(mccw[1])*self._step2rad(1,1)
                except StopMotorInterrupt:
                    keepGoing = False
        else:
            print("Motor is busy!")
    def handleButtonReleaseSignal(self,motor):
        self.motors[motor].motor_stop()
    def gotoAA(self,alt=0,az=0):
        if not self.mLock:
            self.mLock = True
            """if advanced:
                calt = np.cos(alt)
                salt = np.sin(alt)
                caz = np.cos(az)
                saz = np.sin(az)
                newPos = np.array([[caz*calt],[saz*calt],[salt]])*L1 + self.pos0 #TODO: Adjust this for feasability
                try:
                    target = self.inverseK(newPos)
                except NameError: target = (az,alt) #Thus, I don't need to define this function if the mount doesn't require it
            else:"""
            target = (az,alt)
            delta = target - self.theta

            for m in range(2):
                dSteps = self._rad2step(1,delta[m])
                startTime = time.time()
                try:
                    self.motors[m].motor_go(dSteps<0,self.mstep,np.abs(dSteps),self.stepdelay)
                    self.theta[m] += dSteps
                except StopMotorInterrupt:
                    self.theta[m] += (time.time() - startTime) / self.stepdelay
            self.mLock = False
    def constructRaster(self,rad=100):
        if not self.mLock:
            self.goToAA() #Go to center
            self.theta=(0,0)
            self.mLock = True
            self.canReceive = True
            while self.theta[1] < rad:
                baseTime = time.time()
                try:
                    self.theta += (0,self.step2rad(1,1))
                    self.canReceive=True
                    self.motors[0].motor_go(0,self.mstep,self.rad2step(1,60*np.pi,self.stepdelay))
                    time.sleep(self.stepdelay*self.rad2step(1,60*np.pi))
                    self.canReceive=False
                    self.motors[1].motor_go(0,self.mstep,1,self.stepdelay) #Go one step down
                except StopMotorInterrupt:
                    self.goToAA()
                    self.theta = (0,0)
            self.mLock = False
        else:
            print("Motor is busy")

