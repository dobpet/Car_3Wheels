from machine import UART, Pin, Timer
import utime
import binascii
from settings import ESP_Networks
from ESP_DC import ScannedNetwork, STA_Info



class ESP_AT(object):
    
    # private variables
    __lastRxTS = None
    __ESPMessage = None
    
    __ESP_AT_SM_State = 0   # State machine step
    __stationMAC = None
    __acesspointMAC = None
    
    __AP_SSID = None
    __AP_Password = None
    __AP_Channel = None
    __AP_IP = None
    __AP_SM = None
    __DHCP_From = None
    __DHCP_To = None
    
    __stateChangeCallback = None
    __dataReceivedCallback = None
    __state = None
    
    __STAState = STA_Info()
    
    ESP_Created = const(0)
    ESP_Initializing = const(1)
    ESP_Initialized = const(2)
    
    ESP_NetworkScanning = const(3)
    ESP_AvailableNetworksUpdated = const(4)
    
    ESP_AP_Activating = const(5)
    ESP_AP_Activated = const(6)
    
    ESP_STA_Connecting = const(7)
    ESP_STA_ConnectingDone = const(8)
    ESP_STA_KnownNetworkNotFound = const(9)
    
    ESP_ServerStarting = const(10)
    ESP_ServerStarted = const(11)
    
    ESP_Connected = const(12)
    ESP_Disconnected = const(13)
    
    __AvailableNetworks = []
    __TargetNetwork = None
    
    __msgpart = None
    
    __DataForSend = None
    __DataForSendConnection = None
    __BeforeSendState = None
    __HighSpeedTS = None
    
    STA_NetInfo = [None, None, None, None]  # IP, SM, DG, MAC
    
    def CheckRx(self,timer):
        if self.__ESP_AT_SM_State == 3:
            if (utime.ticks_ms() - self.__HighSpeedTS) > 1000:
                self.__SendMessage("AT")
                self.__HighSpeedTS = utime.ticks_ms()
        msg = self._uart.readline()
        if self.__msgpart != None:
            bf = self.__msgpart + msg 
            msg = bf
            self.msgpart = None
        if msg != None:
            if self.__ESPMessage == None:
                self.__lastRxTS = utime.ticks_ms()
                try:
                    msgs = msg[0:4]
                    msgss = msgs.decode('ascii').rstrip()
                    if msgss != "+IPD":
                        self.__ESPMessage = msg.decode('ascii').rstrip()
                        if self.__ESPMessage == "":
                           self.__ESPMessage = None
                    else:
                        self.__ESPMessage = None
                        dppos = msg.find(b'\x3A')
                        if dppos != -1:
                            ipdmsb = msg[0:dppos+1]
                            mstr = ipdmsb.decode('ascii')
                            cparts = mstr.split(",")
                            datalen = int(cparts[2])
                            ipddt = msg[dppos+1:]
                            if len(ipddt) < datalen:
                                self.__msgpart = msg
                            else:
                                self.__msgpart = None;
                                if self._debug:
                                    print(" --> EXP_AT  rx : " + mstr + ' ' + str(binascii.hexlify(ipddt, b' ').decode('ascii').upper() ) )
                                fr = cparts[3] + ":" +cparts[4][:-1]
                                self.__DataReceived(int(cparts[1]), fr, ipddt)
                except UnicodeError:
                    if self._debug:
                        print(" --> EXP_AT ERR : unicode error")
                else:
                    if self.__ESPMessage != None:
                        if self._debug:
                            print(" --> EXP_AT  rx : " + self.__ESPMessage)
                        if self.__ESP_AT_SM_State == 1 or self.__ESP_AT_SM_State == 2:
                            self.__ESPMessage = None
                        else:
                            self.__ProcessMessage()
            else:
                if self._debug:
                    print(" --> EXP_AT ERR : rx overrun")           
        else:
            if self.__DataForSend != None and self.__DataForSendConnection != None and self.__ESP_AT_SM_State == 32:
                self.__BeforeSendState = self.__ESP_AT_SM_State
                self.__SendMessage("AT+CIPSENDEX={0:d},{1:d}".format(self.__DataForSendConnection, len(self.__DataForSend)))
                self.__ESP_AT_SM_State = 40
            if self.__lastRxTS != None:
                if (utime.ticks_ms() - self.__lastRxTS) > 20:
                    if self.__ESP_AT_SM_State == 1:
                        self.__ESP_AT_SM_State = 2
                        self.__lastRxTS = None
                    elif self.__ESP_AT_SM_State == 2:
                        self.__ESP_AT_SM_State = 3
                        self._uart.read()
                        self._uart = UART(self._UARTNumber, baudrate=115200)
                        self.__HighSpeedTS = utime.ticks_ms()
                        if self._debug:
                            print(" --> EXP_AT     : speed changed to 115200 kbps")
            
    
    def __init__ (self, UARTNumber, TXPin, RXPin, ENPin, Debug = True, StateChangeCallback = None,
                  DataReceivedCallback = None):
        self.__stateChangeCallback = StateChangeCallback
        self.__dataReceivedCallback = DataReceivedCallback
        self._debug = Debug;
        self._UARTNumber = UARTNumber
        self._uart = UART(self._UARTNumber, parity = None, stop = 1, bits = 8, rx=RXPin, tx=TXPin,
                          baudrate=76800, rxbuf=1000, timeout=2)
        self._uart.read()
        self.__StateChange(None, ESP_Created)
        self._ENPin = ENPin
        if self._ENPin.value() == 1:
            self._ENPin.value(0)
    
    def ON(self):
        self._tmrRX = Timer()       
        if self._debug:
            print(" --> ESP_AT     : _____ enabling _____")
        if self._ENPin == None:
            print(" --> ESP_AT ERR : EN pin not defined")
        else:
            if self._ENPin.value() == 1:
                print("EN pin is on")
                self._ENPin.value(0)
                utime.sleep_ms(4000)
            self._ENPin.value(1)
        self._tmrRX.init(freq=300, mode=Timer.PERIODIC, callback=self.CheckRx)
        self.__ESP_AT_SM_State = 1
        self.__StateChange(None, ESP_Initializing)
        
    def OFF(self):
        if self._ENPin == None:
            print(" --> ESP_AT ERR : EN pin not defined")
        else:
            if self._debug:
                print(" --> ESP_AT     : _____ disabling _____")
            self._ENPin.value(0)
        self._tmrRX.deinit()
        self.__ESP_AT_SM_State = 0
            
    def __ProcessMessage(self):
        if self.__ESPMessage == 'ERROR':
            if self.__ESP_AT_SM_State == 6:  # AT+CWAUTOCONN=0
                self.__ESPMessage = 'OK'
        if (self.__ESPMessage == 'ready' or self.__ESPMessage == 'OK') and self.__ESP_AT_SM_State == 3:
            self.__ESP_AT_SM_State = 4
            if self._debug:
                print(" --> ESP_AT     : _____ module ready _____")
            self.__SendMessage("+ATE0")
        elif self.__ESPMessage == 'OK' and self.__ESP_AT_SM_State >= 4:
            self.__ESP_AT_SM_State += 1
            print(self.__ESP_AT_SM_State)
            if self.__ESP_AT_SM_State == 5:
                self.__SendMessage("AT+GMR");
            elif self.__ESP_AT_SM_State == 6:
                self.__SendMessage("AT+CWAUTOCONN=0");
            elif self.__ESP_AT_SM_State == 7:
                self.__SendMessage("AT+CIPAPMAC?");
            elif self.__ESP_AT_SM_State == 8:
                self.__SendMessage("AT+CIPSTAMAC?");
            elif self.__ESP_AT_SM_State == 9:
                self.__SendMessage("AT+CWLAPOPT=0,2047");
            elif self.__ESP_AT_SM_State == 10:
                self.__SendMessage("AT+CWMODE=3");
            elif self.__ESP_AT_SM_State == 11:
                self.__SendMessage("AT+CIPMUX=1")
            elif self.__ESP_AT_SM_State == 12:
                self.__SendMessage("AT+CIPDINFO=1")
                self.__ESP_AT_SM_State = 13
            elif self.__ESP_AT_SM_State == 13:
                pass
                #self.__ESP_AT_SM_State = 12
                #self.__SendMessage("AT+CWCOUNTRY_CUR=1,\"CS\",1,10")
            elif self.__ESP_AT_SM_State == 14:
                self.__StateChange(None, ESP_Initialized)
            elif self.__ESP_AT_SM_State == 16:
                self.__StateChange(None, ESP_AvailableNetworksUpdated)
            elif self.__ESP_AT_SM_State == 21:
                if self.__DHCP_From != None and self.__DHCP_To != None:
                    self.__SendMessage("AT+CWDHCPS_CUR=1,120,\"" + self.__DHCP_From + "\",\"" + self.__DHCP_To + "\"")
                else:
                    self.__ESP_AT_SM_State = 22               
            elif self.__ESP_AT_SM_State == 22:
                self.__SendMessage("AT+CWSAP=\""+self.__AP_SSID+"\",\""+self.__AP_Password+"\","+str(self.__AP_Channel)+",4")
            elif self.__ESP_AT_SM_State == 23:
                self.__StateChange(None, ESP_AP_Activated)
            elif self.__ESP_AT_SM_State == 26:
                self.__TargetNetwork = None
                for i in ESP_Networks:
                    for j in self.__AvailableNetworks:
                        if i.SSID == j.SSID:
                            self.__TargetNetwork = i
                            break
                    if self.__TargetNetwork != None:
                        break
                if self.__TargetNetwork == None:
                    self.__ESP_AT_SM_State = 35
                    if self._debug:
                        print(" --> ESP AT     : _____ known network not available _____")
                        self.__StateChange(None, ESP_STA_KnownNetworkNotFound)
                else:
                    self.__StateChange(None, ESP_STA_Connecting)
                    self.__ESP_AT_SM_State = 28
                    if self._debug:
                        print(" --> ESP AT     : _____ starting connection to " + self.__TargetNetwork.SSID + " _____")                         
                    self.__SendMessage("AT+CWJAP=\"" + self.__TargetNetwork.SSID + "\",\"" + self.__TargetNetwork.Password + "\"")
            elif self.__ESP_AT_SM_State == 29:
                self.__SendMessage("AT+CWJAP?")
            elif self.__ESP_AT_SM_State == 30:
                self.__SendMessage("AT+CIPSTA?")
            elif self.__ESP_AT_SM_State == 31:
                self.__StateChange(None, ESP_STA_ConnectingDone)
            elif self.__ESP_AT_SM_State == 46:
                self.__StateChange(None, ESP_ServerStarted)
                self.__ESP_AT_SM_State = 32
        elif self.__ESPMessage.startswith("+CWJAP:"):
            self.__STAState.ParseCWJAP(self.__ESPMessage)
        elif self.__ESPMessage.startswith("+CIPSTAMAC:"):
            self.__STAState.ParseCIPSTAMAC(self.__ESPMessage)
        elif self.__ESPMessage.startswith("+CIPAPMAC:"):
            self.STA_NetInfo[3] = self.__ESPMessage[11:-1].upper()
        elif self.__ESPMessage.startswith("+CIPSTA:"):
            self.__STAState.ParseCIPSTA(self.__ESPMessage)
        elif self.__ESPMessage.startswith("+CWLAP:("):
            _bf = ScannedNetwork(self.__ESPMessage[8:-1])
            self.__AvailableNetworks.append(_bf)
        elif self.__ESPMessage.startswith(">") and self.__ESP_AT_SM_State == 41:
            self.__SendMessage(self.__DataForSend)
            self.__ESP_AT_SM_State = 42
        elif self.__ESP_AT_SM_State == 42:
            if self.__ESPMessage.startswith("SEND OK"):
                pass
            elif self.__ESPMessage.startswith("SEND FAIL"):
                pass
            self.__ESP_AT_SM_State = self.__BeforeSendState
            self.__DataForSend = None
            self.__DataForSendConnection = None
        else:
            cparts = self.__ESPMessage.split(",")
            if len(cparts) == 2:
                if cparts[1] == "CONNECT":
                    if self._debug:
                        print(" --> ESP_AT     : _____  connected   _____")
                    self.__StateChange(int(cparts[0]), ESP_Connected)
                if cparts[1] == "CLOSED":
                    if self._debug:
                        print(" --> ESP_AT     : _____ disconnected _____")
                    self.__StateChange(int(cparts[0]), ESP_Disconnected)
        self.__ESPMessage = None
    
    def __SendMessage(self, Message):
        if self._debug:
            print(" --> ESP_AT  tx :", end = " ")
            if isinstance(Message, bytearray):
                print(binascii.hexlify(Message, b' ').decode('ascii').upper())
            else:
                print(Message)
        self._uart.write(Message + '\r\n')
    
    def __StateChange(self, ConnectionNumber, NewState):
        if self.__stateChangeCallback != None:
            self.__stateChangeCallback(ConnectionNumber, NewState)
        self.__state = NewState
        
    def __DataReceived(self, ConnectionNumber, From, Data):
        if self.__dataReceivedCallback != None:
            self.__dataReceivedCallback(ConnectionNumber, From, Data)
    
    def Scan(self):
        self.__ESP_AT_SM_State = 15
        self.__AvailableNetworks = []
        if self._debug:
            print(" --> ESP_AT     : _____ network scan _____")
        self.__StateChange(None, ESP_NetworkScanning)
        self.__SendMessage("AT+CWLAP")
        
    
    def AP_Activate(self, SSID, Password, Channel, IP, SM, DHCP_From = None, DHCP_To = None):
        self.__StateChange(None, ESP_AP_Activating)
        self.__ESP_AT_SM_State = 20
        self.__AP_SSID = SSID
        self.__AP_Password = Password
        self.__AP_Channel = Channel
        self.__AP_IP = IP
        self.__AP_SM = SM
        self.__DHCP_From = DHCP_From
        self.__DHCP_To = DHCP_To
        self.__SendMessage("AT+CIPAP=\""+self.__AP_IP+"\",\""+self.__AP_IP+"\",\""+self.__AP_SM+"\"")
        
    def STA_Connect(self):
        self.__ESP_AT_SM_State = 25
        self.__AvailableNetworks = []
        self.__StateChange(None, ESP_NetworkScanning)
        self.__SendMessage("AT+CWLAP")
        
    
    def StartServer(self, PortNumber):
        self.__ESP_AT_SM_State = 45
        self.__StateChange(None, ESP_ServerStarting)
        self.__SendMessage("AT+CIPSERVER=1,{0:d}".format(PortNumber))
        
        
    def SendData(self, ConnectionNumber, Data):
        if(self.__DataForSend != None or self.__DataForSendConnection != None):
            if self._debug:
                print(" --> ESP_AT ERR : _____ send overrun _____")
            return False
        else:
            self.__DataForSend = Data
            self.__DataForSendConnection = ConnectionNumber
            return True
            
    def Debug(self, Value):
        self._debug = Value;
        
    @property
    def STA_State(self):
        return self.__STAState
     
    @property
    def IsModuleReady(self):
        if self.__ESP_AT_SM_State > 5:
            return True
        else:
            return False