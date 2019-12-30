import pycom
from network import WLAN, Bluetooth
import urequests
import machine
import ubinascii

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)
bluetooth = Bluetooth()

#Change accordingly
url = 'http://***.hub.ubeac.io/mygateway'
#****************************************

#Change accordingly
wifi_ssid = "abc123"
wifi_pass = "12345678"
#*********************

my_beacons = []

nets = wlan.scan()

connected = False
for net in nets:
    if net.ssid == wifi_ssid:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, wifi_pass), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        connected = True
        break

bluetooth.start_scan(-1)

# wait
while 1:
    adv = bluetooth.get_adv()
    if adv:
        mfg_data = bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)

        if(mfg_data is not None) and (mfg_data not in my_beacons):
            pycom.rgbled(0x0000ff)

            mfg_data = str(ubinascii.hexlify(mfg_data))
            mfg_data = mfg_data.replace('b\'', '').replace('\'','')
            my_beacons.append(mfg_data)

            print(mfg_data)

            my_data = {"Data" : str(my_beacons)}

            if(connected is True):
                res = urequests.post(url, data=str(my_data))
                res.close()
            
            pycom.rgbled(0x000000)
        