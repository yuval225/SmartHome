import socket
import subprocess
import platform
import struct

"""
*CONSTS*
"""

PC_IPADDR = "10.0.0.100"
PC_OPENPORT = 5050
PHONE_IP = '10.0.0.12'
PC_MACADDR = "10:20:30:40:50:60"


def sendMagicPacket():
    """
    function sends a magic packet to wake up the client computer.
    magic packet = 6 Full bytes (FF) + Device mac address.
    """
    splitMac = str.split(PC_MACADDR,':')

    hexMac = struct.pack('BBBBBB', int(splitMac[0], 16),
                                     int(splitMac[1], 16),
                                     int(splitMac[2], 16),
                                     int(splitMac[3], 16),
                                     int(splitMac[4], 16),
                                     int(splitMac[5], 16))

    magicPacket = '\xff' * 6 + hexMac * 16
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
        sock.sendto(magicPacket,(PC_IPADDR,PC_OPENPORT))

 
def ping_ip(current_ip_address):
    """
    Ping a specific ip and return true for successful ping and false for unreachable status
    INPUT: current_ip_adress = IP STRING
    OUTPUT: Bool of connection status
    """
    try:
        output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
        ) == "windows" else 'c', current_ip_address ), shell=True, universal_newlines=True)
        if 'unreachable' in output:
            return False
        else:
            return True
    except Exception:
            return False

if __name__ == '__main__':
    clientStatus = False

    if ping_ip(PHONE_IP):
        print("Client is currently at home.")
        clientStatus = True
    else:
        print("Client isn`t home.")
        clientStatus = False

    prevStatus = clientStatus

    while(True):
        if ping_ip(PHONE_IP):
            print("Client is currently at home.")
            clientStatus = True
        else:
            print("Client isn`t home.")
            clientStatus = False
        if clientStatus != prevStatus and clientStatus:
            print("Client just arrived at home, waking up pc with magic packet.")
            sendMagicPacket()
        prevStatus = clientStatus
