from machine import Pin
import machine
import MotorClass
import ServoClass
import SequencerClass as Sequencer
import program
import buzzer

#Motor init
PinForward = machine.PWM(machine.Pin(9))
PinBackward = machine.PWM(machine.Pin(8))
MotorLeft = MotorClass.MotorClass(PinForward,PinBackward, 1000)

PinForward = machine.PWM(machine.Pin(11))
PinBackward = machine.PWM(machine.Pin(10))
MotorRight = MotorClass.MotorClass(PinForward,PinBackward, 1000)

speed = 0
MotorLeft.SetSpeed(speed)
MotorRight.SetSpeed(speed)

#Servo init
Pin = machine.PWM(machine.Pin(12))
Servo1 = ServoClass.ServoClass(Pin, 2000, 50) #Pin, Ramp, Freq

Pin = machine.PWM(machine.Pin(13))
Servo2 = ServoClass.ServoClass(Pin, 2000, 50) #Pin, Ramp, Freq

Pin = machine.PWM(machine.Pin(14))
Servo3 = ServoClass.ServoClass(Pin, 2000, 50) #Pin, Ramp, Freq

Pin = machine.PWM(machine.Pin(15))
Servo4 = ServoClass.ServoClass(Pin, 2000, 50) #Pin, Ramp, Freq

position = 0
Servo1.SetPosition(position)
Servo4.SetPosition(position)

#Sequencer init
MoveSeq = Sequencer.Sequencer()

StepMove = 1

#buzzer
PinBuzzer = machine.PWM(machine.Pin(22))

Buzzer1 = buzzer.Buzzer(PinBuzzer)
Buzzer1.EnableBuzzer(buzzer.songBeep)#songPacman)

def ProgramFce(Program): #for calling have to StepMove > 0
    global StepMove
    global Servo1
    global Servo2
    global Servo3
    global Servo4
    global MotorLeft
    global MotorRight
    ProgStep = StepMove - 1
    """
    print("krok = " + str(ProgStep) +
          " MotorL = " + str(Program[ProgStep].MotorL) +
          " MotorR = " + str(Program[ProgStep].MotorR) +
          " Servo1 = " + str(Program[ProgStep].Servo1) +
          " Servo2 = " + str(Program[ProgStep].Servo2) +
          " Servo3 = " + str(Program[ProgStep].Servo3) +
          " Servo4 = " + str(Program[ProgStep].Servo4))
    """
    Servo1.SetPosition(Program[ProgStep].Servo1)
    Servo2.SetPosition(Program[ProgStep].Servo2)
    Servo3.SetPosition(Program[ProgStep].Servo3)
    Servo4.SetPosition(Program[ProgStep].Servo4)
    MotorLeft.SetSpeed(Program[ProgStep].MotorL)
    MotorRight.SetSpeed(Program[ProgStep].MotorR)
    
    StepMove = StepMove + 1
    if StepMove >= len(Program):
        StepMove = 1
    StepMove = MoveSeq.SetNextStep(StepMove, Program[ProgStep].Time)
           
#cyclic 
while True:
    #for update value for components
    MotorLeft.SpeedUpdate()
    MotorRight.SpeedUpdate()
    Servo1.PositionUpdate()
    Servo2.PositionUpdate()
    Servo3.PositionUpdate()
    Servo4.PositionUpdate()
    Buzzer1.BuzzerUpdate()

    StepMove = MoveSeq.SequencerUpdater(StepMove)
    
    #program
    if StepMove > 0:
        ProgramFce(program.Program2)

    """
    if (Servo1.GetActualPosition() >= 100):
        Servo1.SetPosition(0)
    elif (Servo1.GetActualPosition() <= 0):
        Servo1.SetPosition(100)
    """  
        
    """
    if StepMove == 1:
        Servo1.SetPosition(0)
        MotorLeft.SetSpeed(30000)
        MotorRight.SetSpeed(0)
        StepMove = MoveSeq.SetNextStep(2, 5000)
    elif StepMove == 2:
        Servo1.SetPosition(25)
        MotorLeft.SetSpeed(0)
        MotorRight.SetSpeed(0)
        StepMove = MoveSeq.SetNextStep(3, 5000)
    if StepMove == 3:
        Servo1.SetPosition(50)
        MotorLeft.SetSpeed(0)
        MotorRight.SetSpeed(30000)
        StepMove = MoveSeq.SetNextStep(4, 5000)
    elif StepMove == 4:
        Servo1.SetPosition(75)
        MotorLeft.SetSpeed(0)
        MotorRight.SetSpeed(0)
        StepMove = MoveSeq.SetNextStep(5, 5000)
    elif StepMove == 5:
        Servo1.SetPosition(100)
        MotorLeft.SetSpeed(30000)
        MotorRight.SetSpeed(-30000)
        StepMove = MoveSeq.SetNextStep(6, 5000)
    elif StepMove == 6:
        Servo1.SetPosition(75)
        MotorLeft.SetSpeed(0)
        MotorRight.SetSpeed(0)
        StepMove = MoveSeq.SetNextStep(7, 5000)
    elif StepMove == 7:
        Servo1.SetPosition(50)
        MotorLeft.SetSpeed(-30000)
        MotorRight.SetSpeed(30000)
        StepMove = MoveSeq.SetNextStep(1, 5000)
    """
        
    """    
    MotorLeft.SpeedUpdate()
    if (MotorLeft.GetActualSpeed() >= speed):
        MotorLeft.SetSpeed(-speed)
    elif (MotorLeft.GetActualSpeed() <= -speed):
        MotorLeft.SetSpeed(speed)
        
    MotorRight.SpeedUpdate()
    if (MotorRight.GetActualSpeed() >= speed):
        MotorRight.SetSpeed(-speed)
    elif (MotorRight.GetActualSpeed() <= -speed):
        MotorRight.SetSpeed(speed)
    """