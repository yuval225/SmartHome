import socket
import subprocess
import platform

"""
*CONSTS*
"""

PC_IPADDR = "10.0.0.100"
PC_OPENPORT = 5050
PHONE_IP = '10.0.0.12'
PC_MACADDR = "ENTER PC MAC ADDRESS"


def sendMagicPacket():
    """
    function sends a magic packet to wake up the client computer.
    magic packet = 6 Full bytes (FF) + Device mac address.
    """
    magicMessage = "FFFFFFFFFFFF" + PC_MACADDR.replace(':','')
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(bytes.fromhex(magicMessage),(PC_IPADDR,PC_OPENPORT))

 
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
        print("Client is connected to wifi")
        clientStatus = True
    else:
        print("Client is disconnected from wifi")
        clientStatus = False

    prevStatus = clientStatus

    while(True):
        if ping_ip(PHONE_IP):
            print("Client is connected to wifi")
            clientStatus = True
        else:
            print("Client is disconnected from wifi")
            clientStatus = False
        if clientStatus != prevStatus and clientStatus:
            sendMagicPacket()
        prevStatus = clientStatus
