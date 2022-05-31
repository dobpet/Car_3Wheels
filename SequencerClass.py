import utime

class Sequencer:
    __TimeOfStart = 0
    __TimeToNextStep = 0
    
    __NextStep = 0
    __Run = False
    
    def __init__(self): 
        self.__TimeOfStart = utime.ticks_ms()   
    
    def __TimeAction(self):
        #print("Sequencer: RUN " + str(utime.ticks_ms() - self.__TimeOfStart) + ", " + str(self.__TimeToNextStep))        
        if (utime.ticks_ms() - self.__TimeOfStart) > self.__TimeToNextStep:
            #self.__Run = False
            return True
        else:
            return False
        
    def SetNextStep(self, NextStep, TimeToNextStep):
        self.__NextStep = NextStep
        self.__TimeToNextStep = TimeToNextStep
        #self.__TimeOfStart = utime.ticks_ms()
        #self.__Run = True
        #return 0 #Step 0 == waiting
        
    def SequencerUpdater(self, ActualStep):
        if self.__Run:
            if self.__TimeAction():
                self.__TimeOfStart = utime.ticks_ms()
                return self.__NextStep
            else:
                return ActualStep
        else:
            return ActualStep
                
    def Stop(self):
        self.__NextStep = 0
        self.__TimeToNextStep = utime.ticks_ms()
        self.__TimeOfStart = utime.ticks_ms()
        self.__Run = False
    
    def Start(self):
        self.__TimeOfStart = utime.ticks_ms()
        self.__Run = True
        
    def GetRun(self):
        return self.__Run

                
                
                