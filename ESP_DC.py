class Network:
    __SSID = ""
    __Password = ""
    __IP = None
    __SM = None
    __DG = None
    
    def __init__(self, SSID, Password, IP = None, SM = None, DG = None):
        self.__SSID = SSID
        self.__Password = Password
        self.__IP = IP
        self.__SM = SM
        self.__DG = DG
    
    @property
    def SSID(self):
        return self.__SSID

    @property
    def Password(self):
        return self.__Password
    
    @property
    def IP(self):
        return self.__IP
    
    @property
    def SM(self):
        return self.__SM
    
    @property
    def DG(self):
        return self.__DG

class ScannedNetwork:
    __SSID = ""
    __EncMethod = ""
    __RSSI = -100
    __MAC = ""
    __Channel = 0
    
    def __init__(self, CWLAP_Sentence):
        _parts = CWLAP_Sentence.split(",")
        self.__SSID = _parts[1][1:-1]
        if _parts[0] == "0":
            self.__EncMethod = "OPEN"
        elif _parts[0] == "1":
            self.__EncMethod = "WEP"
        elif _parts[0] == "2":
            self.__EncMethod = "WPA_PSK"
        elif _parts[0] == "3":
            self.__EncMethod = "WPA2_PSK"
        elif _parts[0] == "4":
            self.__EncMethod = "WPA_WPA2_PSK"
        elif _parts[0] == "5":
            self.__EncMethod = "WPA2_ENTERPRISE"
        elif _parts[0] == "6":
            self.__EncMethod = "WPA3_PSK"
        elif _parts[0] == "7":
            self.__EncMethod = "WPA2_WPA3_PSK"
        else:
            self.__EncMethod = "? " + _parts[1] + " ?"
        self.__RSSI = int(_parts[2])
        self.__MAC = _parts[3][1:-1].upper()
        self.__Channel = int(_parts[4])
        
    @property
    def SSID(self):
        return self.__SSID
    
    def __repr__(self):
        return self.__SSID + " ( Ch " + str(self.__Channel) + "  RSSI " + str(self.__RSSI) + "dBm  " + self.__EncMethod + "  " + self.__MAC + " )"
    
class STA_Info:
    __SSID = None
    __APMAC = None
    __STAMAC = None
    __Channel = None
    __RSSI = None
    __IP = None
    __SM = None
    __DG = None
    
    def ParseCWJAP(self, CWJAP):
        #+CWJAP:"Pidisvet","e4:be:ed:4d:7c:29",6,-64
        _dat = CWJAP[7::]
        _parts = _dat.split(",")
        self.__SSID = _parts[0][1:-1]
        self.__APMAC = _parts[1][1:-1].upper()
        self.__Channel = int(_parts[2])
        self.__RSSI = int(_parts[3])
        
    def ParseCIPSTA(self, CIPSTA):
        if CIPSTA.startswith("+CIPSTA:ip:"):
            self.__IP = CIPSTA[12:-1].upper()
        elif CIPSTA.startswith("+CIPSTA:gateway:"):
            self.__DG = CIPSTA[17:-1].upper()
        elif CIPSTA.startswith("+CIPSTA:netmask:"):
            self.__SM = CIPSTA[17:-1].upper()
    
    def ParseCIPSTAMAC(self, CIPSTAMAC):
        self.__STAMAC = CIPSTAMAC[12:-1].upper()
    
    @property
    def SSID(self):
        return self.__SSID
    
    @property
    def APMAC(self):
        return self.__APMAC
    
    @property
    def STAMAC(self):
        return self.__STAMAC
    
    @property
    def Channel(self):
        return self.__Channel
    
    @property
    def RSSI(self):
        return self.__RSSI
    
    @property
    def IP(self):
        return self.__IP
    
    @property
    def SM(self):
        return self.__SM
    
    @property
    def DG(self):
        return self.__DG