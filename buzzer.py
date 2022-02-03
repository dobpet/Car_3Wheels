"""
Autoupdate:
    - BuzzerUpdate(self)
Enable play:
    - EnableBuzzer(self, song):
Disable:
    - DisableBuzzer(self):
    
Example:
    from time import sleep
    from machine import Pin
    import buzzer

    PinBuzzer = machine.PWM(Pin(22))

    Buzzer1 = buzzer.Buzzer(PinBuzzer)
    Buzzer1.EnableBuzzer(buzzer.songPacman)

    while True:
        
        Buzzer1.BuzzerUpdate()
"""

from machine import Pin, PWM
import utime
#from utime import sleep

songBeep = ["C4", 8, "C3", 16, "P", 1,"P", 1,"P", 1]
#source of songs: https://github.com/robsoncouto/arduino-songs
songFurEllise = ["E4",8,"DS4",8,"E4",8,"DS4",8,"E4",8,"B3",8,"D4",8,"C4",8,"A3",8,"A3",8,"A3",8,"D3",8,"F3",8,"A3",8,"B3",8,"B3",8,"B3",8,"F3",8,"AS3",8,"B3",8,"C4",8,"C4",8,"C4",8,"C4",8,"E4",8,"DS4",8,"E4",8,"DS4",8,"E4",8,"B3",8,"D4",8,"C4",8,"A3",8,"A3",8,"A3",8,"D3",8,"F3",8,"A3",8,"B3",8,"B3",8,"B3",8,"F3",8,"C4",8,"B3",8,"A3",8,"A3",8,"A3",8,"B3",8,"C4",8,"D4",8,"E4",8,"E4",8,"E4",8,"G3",8,"F4",8,"E4",8,"D4",8,"D4",8,"D4",8,"E3",8,"E4",8,"D4",8,"C4",8,"C4",8,"C4",8,"D3",8,"D4",8,"C4",8,"B3",8,"B3",8,"B3",8,"B3",8,"E4",8,"DS4",8,"E4",8,"DS4",8,"E4",8,"B3",8,"D4",8,"C4",8,"A3",8,"A3",8,"A3",8,"D3",8,"F3",8,"A3",8,"B3",8,"B3",8,"B3",8,"F3",8,"A3",8,"B3",8,"C4",8,"C4",8,"C4",8,"C4",8,"E4",8,"DS4",8,"E4",8,"DS4",8,"E4",8,"B3",8,"D4",8,"C4",8,"A3",8,"A3",8,"A3",8,"D3",8,"F3",8,"A3",8,"B3",8,"B3",8,"B3",8,"F3",8,"C4",8,"B3",8,"A3",8,"A3",8,"A3"   ]#
songPacman = [ "B4", 16, "B5", 16, "FS5", 16, "DS5", 16, "B5", 32, "FS5", -16, "DS5", 8, "C5", 16, "C6", 16, "G6", 16, "E6", 16, "C6", 32, "G6", -16, "E6", 8,"B4", 16,  "B5", 16,  "FS5", 16,   "DS5", 16,  "B5", 32,"FS5", -16, "DS5", 8,  "DS5", 32, "E5", 32,  "F5", 32,"F5", 32,  "FS5", 32,  "G5", 32,  "G5", 32, "GS5", 32,  "A5", 16, "B5", 8]
songNokia = ["E5", 8, "D5", 8, "FS4", 4, "GS4", 4, "CS5", 8, "B4", 8, "D4", 4, "E4", 4, "B4", 8, "A4", 8, "CS4", 4, "E4", 4,"A4", 2 ]
songStarWars = ["AS4",8, "AS4",8, "AS4",8,"F5",2, "C6",2,"AS5",8, "A5",8, "G5",8, "F6",2, "C6",4,"AS5",8, "A5",8, "G5",8, "F6",2, "C6",4,"AS5",8, "A5",8, "AS5",8, "G5",2, "C5",8, "C5",8, "C5",8,"F5",2, "C6",2,"AS5",8, "A5",8, "G5",8, "F6",2, "C6",4,"AS5",8, "A5",8, "G5",8, "F6",2, "C6",4, "AS5",8, "A5",8, "AS5",8, "G5",2, "C5",-8, "C5",16, "D5",-4, "D5",8, "AS5",8, "A5",8, "G5",8, "F5",8,"F5",8, "G5",8, "A5",8, "G5",4, "D5",8, "E5",4,"C5",-8, "C5",16,"D5",-4, "D5",8, "AS5",8, "A5",8, "G5",8, "F5",8,"C6",-8, "G5",16, "G5",2, "P",8, "C5",8,"D5",-4, "D5",8, "AS5",8, "A5",8, "G5",8, "F5",8,"F5",8, "G5",8, "A5",8, "G5",4, "D5",8, "E5",4,"C6",-8, "C6",16,"F6",4, "DS6",8, "CS6",4, "C6",8, "AS5",4, "GS5",8, "G5",4, "F5",8,"C6",1]
    
class Buzzer:
    
    tones = {
    "B0": 31,
    "C1": 33,
    "CS1": 35,
    "D1": 37,
    "DS1": 39,
    "E1": 41,
    "F1": 44,
    "FS1": 46,
    "G1": 49,
    "GS1": 52,
    "A1": 55,
    "AS1": 58,
    "B1": 62,
    "C2": 65,
    "CS2": 69,
    "D2": 73,
    "DS2": 78,
    "E2": 82,
    "F2": 87,
    "FS2": 93,
    "G2": 98,
    "GS2": 104,
    "A2": 110,
    "AS2": 117,
    "B2": 123,
    "C3": 131,
    "CS3": 139,
    "D3": 147,
    "DS3": 156,
    "E3": 165,
    "F3": 175,
    "FS3": 185,
    "G3": 196,
    "GS3": 208,
    "A3": 220,
    "AS3": 233,
    "B3": 247,
    "C4": 262,
    "CS4": 277,
    "D4": 294,
    "DS4": 311,
    "E4": 330,
    "F4": 349,
    "FS4": 370,
    "G4": 392,
    "GS4": 415,
    "A4": 440,
    "AS4": 466,
    "B4": 494,
    "C5": 523,
    "CS5": 554,
    "D5": 587,
    "DS5": 622,
    "E5": 659,
    "F5": 698,
    "FS5": 740,
    "G5": 784,
    "GS5": 831,
    "A5": 880,
    "AS5": 932,
    "B5": 988,
    "C6": 1047,
    "CS6": 1109,
    "D6": 1175,
    "DS6": 1245,
    "E6": 1319,
    "F6": 1397,
    "FS6": 1480,
    "G6": 1568,
    "GS6": 1661,
    "A6": 1760,
    "AS6": 1865,
    "B6": 1976,
    "C7": 2093,
    "CS7": 2217,
    "D7": 2349,
    "DS7": 2489,
    "E7": 2637,
    "F7": 2794,
    "FS7": 2960,
    "G7": 3136,
    "GS7": 3322,
    "A7": 3520,
    "AS7": 3729,
    "B7": 3951,
    "C8": 4186,
    "CS8": 4435,
    "D8": 4699,
    "DS8": 4978
    }
   
    melody = None
    
    note = 0
    enable = False
    
    LastInterTime = 0 # Last Time from intervention
    TimeOfTone = 0
    PinBuzzer = None
    Volume = 800
    
    def __init__(self, PinBuzzer):
        self.PinBuzzer = PinBuzzer#PWM(Pin(22))
    
    def TimeAction(self):
        if (utime.ticks_ms() - self.LastInterTime) > self.TimeOfTone:
            self.LastInterTime = utime.ticks_ms()
            return True
        else:
            return False
    
    def bequiet(self):
        self.PinBuzzer.duty_u16(0)
    
    def playtone(self, frequency):
        self.PinBuzzer.duty_u16(self.Volume)
        self.PinBuzzer.freq(frequency)
    
    def EnableBuzzer(self, song):
        self.melody = song
        self.enable = True
    
    def DisableBuzzer(self):
        self.enable = False
        
    def ChangeTone(self):
        if self.TimeAction():
            notes = len(self.melody) / 2
            if (self.note < notes):
                if (self.melody[self.note] == "P"):
                    self.bequiet()
                else:
                    self.playtone(self.tones[self.melody[self.note]])
                               
                tempo = 105
                wholenote = (60000 * 4) / tempo
                self.TimeOfTone = (wholenote) / abs(self.melody[self.note + 1])

                self.note = self.note + 2
                
            else:
                self.note = 0
                self.bequiet()
        """
        else:
            self.note = 0
            self.bequiet()
        """
            
    def BuzzerUpdate(self):
        
        if self.enable:
            self.ChangeTone()
        else:
            self.bequiet()
            self.note = 0
            
"""




def playsong(mysong):
    global note
    if enable:
        #print("buzzer2 run")
        if (note < len(mysong)):
            if (mysong[note] == "P"):
                bequiet()
            else:
                playtone(tones[mysong[note]])
        else:
            note = 0
            bequiet()
    else:
        note = 0
        bequiet()
    note = note + 1
#while True:
#playsong(song)c
"""