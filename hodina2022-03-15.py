from machine import Pin, I2C, PWM
import MotorClass
import ServoClass
import SequencerClass as Sequencer
import program
import buzzer
from ESP_AT import ESP_AT
from settings import *
import Font
from SH1106 import SH1106_I2C
import gc

#Motor init
PinForward = PWM(Pin(9))
PinBackward = PWM(Pin(8))
MotorLeft = MotorClass.MotorClass(PinForward,PinBackward, 1000)

PinForward = PWM(Pin(11))
PinBackward = PWM(Pin(10))
MotorRight = MotorClass.MotorClass(PinForward,PinBackward, 1000)

speed = 0
MotorLeft.SetSpeed(speed)
MotorRight.SetSpeed(speed)

#Servo init
pPin = PWM(Pin(12))
Servo1 = ServoClass.ServoClass(pPin, 2000, 50) #Pin, Ramp, Freq

pPin = PWM(Pin(13))
Servo2 = ServoClass.ServoClass(pPin, 2000, 50) #Pin, Ramp, Freq

pPin = PWM(Pin(14))
Servo3 = ServoClass.ServoClass(pPin, 2000, 50) #Pin, Ramp, Freq

pPin = PWM(Pin(15))
Servo4 = ServoClass.ServoClass(pPin, 2000, 50) #Pin, Ramp, Freq

position = 0
Servo1.SetPosition(position)
Servo4.SetPosition(position)

#Sequencer init
MoveSeq = Sequencer.Sequencer()

StepMove = 1

#buzzer
PinBuzzer = PWM(Pin(22))

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
    #print("krok = " + str(ProgStep) +
    #      " MotorL = " + str(Program[ProgStep].MotorL) +
    #      " MotorR = " + str(Program[ProgStep].MotorR) +
    #      " Servo1 = " + str(Program[ProgStep].Servo1) +
    #      " Servo2 = " + str(Program[ProgStep].Servo2) +
    #      " Servo3 = " + str(Program[ProgStep].Servo3) +
    #      " Servo4 = " + str(Program[ProgStep].Servo4))
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


# BUSES INITIALIZATION                                                                             #
print("--> initializing internal I2C     ... ",end = "")
int_i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
print("done")
print("      - {}".format(int_i2c))
print("      - I2C scanning              ... ",end = "")
int_i2c_dev = int_i2c.scan()

print("done")
print(int_i2c_dev)

#display
DisplayedScreen = None
RequuestedScreen = None

print("--> initializing display          ... ",end = "")
disp = None
if 0x3C in int_i2c_dev:
    disp = SH1106_I2C(128, 64, int_i2c, rotate=180)      # oled controller
    disp.fill(0)
    disp.contrast(30)
    Font.PrintString(disp, SystemName, int((128 - (len(SystemName) * 12)) / 2), 0, 2, 1)
    disp.hline(0,18,128, 1)
    disp.show()
    print("done")
else:
    print("fail")
    print("    !!! NOT FOUND ON BUS !!!")
 
# WIFI INITIALIZATION                                                                              #
esp = None
if disp != None and DisplayedScreen == None:
    Font.PrintString(disp, "WIFI INITIALIZATION", 8, 26, 1, 1)
    Font.PrintString(disp, "SETTING ESP", 30, 45, 1, 1)
    disp.show()
### CALLBACKS 
### State change callback
def WiFi_StateChange(Connection, NewState):
    global esp, ReadyForConnect, Disconnected_ts
    gc.collect()
    if esp != None:
        if Connection == None:
            if NewState == esp.ESP_Initialized:
                if disp != None and DisplayedScreen == None:
                    disp.fill_rect(0, 44, 127, 16, 0)
                    Font.PrintString(disp, "ACTIVATING AP", 24, 45, 1, 1)
                    disp.show()
                esp.AP_Activate(SSID = SystemName,
                                Password = WiFi_AP_Password,
                                Channel = WiFi_AP_Channel,
                                IP = WiFi_AP_IP,
                                SM = WiFi_AP_SM,
                                DHCP_From = WiFi_AP_DHCP_From,
                                DHCP_To = WiFi_AP_DHCP_To)
            elif NewState == esp.ESP_AP_Activated:
                esp.STA_Connect()
            elif NewState == esp.ESP_NetworkScanning:
                if disp != None and DisplayedScreen == None:
                    disp.fill_rect(0, 44, 127, 16, 0)
                    Font.PrintString(disp, "NETWORK SCANNING", 15, 45, 1, 1)
                    disp.show()
            elif NewState == esp.ESP_STA_Connecting:
                if disp != None and DisplayedScreen == None:
                    disp.fill_rect(0, 44, 127, 16, 0)
                    Font.PrintString(disp, "STA CONNECTING", 20, 45, 1, 1)
                    disp.show()
            elif NewState == esp.ESP_STA_ConnectingDone:
                esp.StartServer(502)
            elif NewState == esp.ESP_ServerStarted:
                esp.Debug(False)
                ReadyForConnect = True
                if disp != None and DisplayedScreen == None:
                    disp.fill_rect(0, 26, 127, 38, 0)
                    Font.PrintString(disp, "WIFI READY", 32, 26, 1, 1)
                    Font.PrintString(disp, "WAIT FOR CONNECTION", 5, 45, 1, 1)
                    Font.PrintString(disp, esp.STA_NetInfo[0], 20, 55, 1, 1)
                    disp.show()
                #NeoSequencer.StartSequence( 1, False)
        elif Connection == 0:
            if NewState == esp.ESP_Connected:
                ReadyForConnect = False
                Disconnected_ts = None
                #NeoSequencer.StartSequence( 2, False)
            elif NewState == esp.ESP_Disconnected:
                Disconnected_ts = utime.ticks_ms()

                
  # Data Received callback
def WiFi_DataReceived(ConnectionNumber, From, Data):
    print(Data)
    pass
"""    if ConnectionNumber == 0:
        TxData = Modbus.ProcessMessage(Data)
        if TxData != None:
            esp.SendData( 0, TxData)"""
            
### INITIALIZING ESP ###############################################################################            
esp = ESP_AT(0, Pin(0), Pin(1), Pin(6, Pin.OUT), #ESP_TX, ESP_RX, ESP_EN,
             Debug=True,
             StateChangeCallback = WiFi_StateChange,
             DataReceivedCallback = WiFi_DataReceived)

### SWITCH ON (ENABLE) ESP MODULE ##################################################################
esp.ON()


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
    #Buzzer1.DisableBuzzer()
    
    #program
    if StepMove > 0:
        ProgramFce(program.Program2)

  
