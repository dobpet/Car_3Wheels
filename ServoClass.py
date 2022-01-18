"""
constructor:
    - instance = ServoClass(self, Pin, Ramp, Freq):
methode for cyclic function:
    - instance.PositionUpdate()
control of motor:
    - instance.SetPosition(position) //speed in range 0-100%
read actual speed:
    - speed = instance.GetActualPosition()

example:

    Pin = machine.PWM(machine.Pin(12))
    Servo = ServoClass.ServoClass(Pin, 5000, 50)

    position = 0
    Servo.SetPosition(position)

    while True:
        
        Servo.PositionUpdate()
        if (Servo.GetActualPosition() >= 100):
            Servo.SetPosition(0)
        elif (Servo.GetActualPosition() <= 0):
            Servo.SetPosition(100)
"""
from machine import Pin
import utime

class ServoClass:

    __ActualPosition = 0
    __ReqPosition = 0
    
    __ActualDuty = 0
    __ReqDuty = 0
    
    __Ramp = 5000 #time from 0% to 100% of position
    
    MinDuty = 1600
    MaxDuty = 8400
    
    __Pin = None    #machine.PWM(machine.Pin(x))
    
    __LastInterTime = 0 # Last Time from intervention
    __RegP = 1000    # regulation parameter
    __RegT = 30    # ms regulation parameter
    
    def SetRamp(self, Ramp):
        self.__Ramp = Ramp
        temp = Ramp / self.__RegT
        self.__RegP = int((self.MaxDuty-self.MinDuty) / temp)
        
    def __init__(self, Pin, Ramp, Freq): #freq 50
        self.__Pin = Pin
        self.__Pin.freq(Freq)
        
        self.SetRamp(Ramp)
    
    def __TimeAction(self):
        if (utime.ticks_ms() - self.__LastInterTime) > self.__RegT:
            self.__LastInterTime = utime.ticks_ms()
            return True
        else:
            return False
        
    def SetPosition(self, Position): # 0-100 -> Duty
        if ((Position <= 100) or (Position >= 0)):
            self.__ReqPosition = Position
            self.__ReqDuty = (self.__ReqPosition / 100) * (self.MaxDuty - self.MinDuty) + self.MinDuty
    
    def GetActualPosition(self):
        self.__ActualPosition = ((self.__ActualDuty - self.MinDuty) / (self.MaxDuty - self.MinDuty)) * 100
        return(self.__ActualPosition)
    
    def PositionCalculate(self):
        if self.__TimeAction():
            
            """ linear calculation of position change"""
            if (((self.__ActualDuty - self.__ReqDuty) < self.__RegP) and (abs(self.__ActualDuty - self.__ReqDuty) >= self.__RegP )):                
                self.__ActualDuty = self.__ActualDuty + self.__RegP
            elif (((self.__ActualDuty - self.__ReqDuty) > self.__RegP) and (abs(self.__ActualDuty - self.__ReqDuty) >= self.__RegP )):
                self.__ActualDuty = self.__ActualDuty - self.__RegP
            else:
                self.__ActualDuty = self.__ReqDuty

            """ set maximum speed for command """   
            if (self.__ActualDuty > self.MaxDuty):
                self.__ActualDuty = self.MaxDuty
            elif (self.__ActualDuty < - self.MaxDuty):
                self.__ActualDuty = - self.MaxDuty
            
            #print("DutyCalculate: actual " + str(self.__ActualDuty) + " request " + str(self.__ReqDuty))
       
    def MoveTo(self, Duty):
        self.__Pin.duty_u16(int(Duty))
      
    def PositionUpdate(self):
        self.PositionCalculate()
        self.MoveTo(self.__ActualDuty)
        
