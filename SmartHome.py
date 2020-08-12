import socket
import subprocess
import platform
import struct

"""
*CONSTS*
"""

PC_IPADDR = "10.0.0.100"
PC_OPENPORT = 7
PHONE_IP = '10.0.0.12'
PC_MACADDR = "10:20:30:40:50:60"


def sendMagicPacket():
    """
    function sends a magic packet to wake up the client computer.
    magic packet = 6 Full bytes (FF) + Device mac address.
    """
    macAddr = PC_MACADDR.replace(PC_MACADDR[2],'')
    magicPacket = bytes.fromhex("FF" * 6 + macAddr * 16)
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
            #Actions to do when client arrive home
            print("Client just arrived at home, waking up pc with magic packet.")
            sendMagicPacket()
        elif clientStatus != prevStatus and not clientStatus:
            #Actions to do when client leaves home
            print("Client just left home")

        prevStatus = clientStatus
