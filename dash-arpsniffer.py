import socket
import struct
import binascii

import requests

import time

buttons = {}

def send_data(mac_address):
    url = '<YOUR_BACKEND_ENDPOINT>'
    #Enter relevant request body here
    data = '{"id":"'+mac_address+'"}'
    print data
    r = requests.post(url, data=data)
    print ("status: ", r.status_code)
    buttons[mac_address] = int(round(time.time() * 1000))
    return

#Ensures that the time limit between subsequent button presses is at least 10 seconds
def button_press(mac_address):
    if mac_address in buttons.keys():
        if int(round(time.time() * 1000)) - buttons[mac_address] > 10000:
            send_data(mac_address)  
    else:
        send_data(mac_address)
        return 

rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))

while True:

    packet = rawSocket.recvfrom(2048)

    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)

    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)

    # skip non-ARP packets
    ethertype = ethernet_detailed[2]
    if ethertype != '\x08\x06':
        continue

    source_mac = binascii.hexlify(arp_detailed[5])

    if "<BUTTON_MAC_ADDRESS>"==source_mac:
        print "Amazon Dash button pressed! Souce: ", source_mac
        button_press(source_mac)
