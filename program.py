class ProgramClass:
    __Time = 0
    __MotorL = 0
    __MotorR = 0
    __Servo1 = 0
    __Servo2 = 0
    __Servo3 = 0
    __Servo4 = 0
    
    def __init__(self, Time, MotorL, MotorR, Servo1, Servo2 = None, Servo3 = None, Servo4 = None):
        self.__Time = Time
        self.__MotorL = MotorL
        self.__MotorR = MotorR
        self.__Servo1 = Servo1
        self.__Servo2 = Servo2
        self.__Servo3 = Servo3
        self.__Servo4 = Servo4        
        
    @property
    def Time(self):
        return self.__Time
    
    @property
    def MotorL(self):
        return self.__MotorL
    
    @property
    def MotorR(self):
        return self.__MotorR
    
    @property
    def Servo1(self):
        return self.__Servo1
    
    @property
    def Servo2(self):
        return self.__Servo2
    
    @property
    def Servo3(self):
        return self.__Servo3
    
    @property
    def Servo4(self):
        return self.__Servo4

ProgramStop = (
        ProgramClass( 5000, 00000, 00000, 000, 000, 000, 000 ),
        ProgramClass( 5000, 00000, 00000, 000, 000, 000, 000 ),
        )
Program1 = (
        #Time, MotorL, MotorR, Servo1
        ProgramClass( 5000, 30000, 00000, 000, 000, 000, 000 ),
        ProgramClass( 5000, 00000, 00000, 025, 000, 000, 010),
        ProgramClass( 5000, 00000, 30000, 050, 000, 000, 020),
        ProgramClass( 5000, 00000, 00000, 075, 000, 000, 030),
        ProgramClass( 5000, 30000,-30000, 100, 000, 000, 040),
        ProgramClass( 5000, 00000, 00000, 075, 000, 000, 050),
        ProgramClass( 5000,-30000, 30000, 050, 000, 000, 060),
        ProgramClass( 5000, 00000, 00000, 025, 000, 000, 070),
        )

Program2 = (
        #Time, MotorL, MotorR, Servo1
        ProgramClass( 5000, 00000, 00000, 001, 000, 000, 000 ),
        ProgramClass( 5000, 00000, 00000, 025, 000, 000, 010),
        ProgramClass( 5000, 00000, 00000, 050, 000, 000, 020),
        ProgramClass( 5000, 00000, 00000, 075, 000, 000, 030),
        ProgramClass( 5000, 00000, 00000, 100, 000, 000, 040),
        ProgramClass( 5000, 00000, 00000, 075, 000, 000, 050),
        ProgramClass( 5000, 00000, 00000, 050, 000, 000, 060),
        ProgramClass( 5000, 00000, 00000, 025, 000, 000, 070),
        )
