# boot.py -- run on boot-up
import network
import wifi_credentials


def do_connect():

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi_credentials.ssid, wifi_credentials.password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()
