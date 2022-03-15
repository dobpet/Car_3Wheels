from ESP_DC import Network

SystemName           = "HAL9000001" #11 char


WiFi_AP_Password     = "VaseHeslo"
WiFi_AP_Channel      = 8
WiFi_AP_IP           = "192.168.50.254"
WiFi_AP_SM           = "255.255.255.0"
WiFi_AP_DHCP_From    = "192.168.50.200"
WiFi_AP_DHCP_To      = "192.168.50.210"

ESP_Networks = (    
        Network(SSID="BTECH RV4 demo",
                Password="10knedLiku"
                ),
        
        Network(SSID="VaseDomaciSSID",
                Password="VaseHeslo",
                #IP="192.168.2.10",
                #SM="255.255.255.0",
                #DG="192.168.2.254"
                ),        
        )