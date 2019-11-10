import socket
from struct import *
import sys

PROTO_TCP=6
PROTO_UDP=7

def PacketExtractor(packet):
    stripped_packet=packet[0:20]
    unpacked=unpack('!BBHHHBBH4s4s',stripped_packet)

    version_HeaderLength=unpacked[0]
    version=version_HeaderLength >> 4
    TOS=unpacked[1]
    entire_Length=unpacked[2]
    id=unpacked[3]
    flags=unpacked[4]
    TTL=unpacked[5]
    Upper_protocol=unpacked[6]
    checksum=unpacked[7]
    sourceIP=unpacked[8]
    destIP=unpacked[9]


    #convert into a doted notation
    sourceIP=socket.inet_ntoa(sourceIP)
    destIP=socket.inet_ntoa(destIP)


    if Upper_protocol==PROTO_TCP:
        tcp=unpack('!HHLLBBHHH',Upper_protocol)

        sourcePort=tcp[0]
        destPort=tcp[1]
        seqenceNumber=tcp[2]
        ackNumber=tcp[3]
        reserver=tcp[4]
        hederLength=tcp[5]
        flags=tcp[6]
        FIN=flags & 0x01
        SYN=(flags >>1) & 0x01
        RST=(flags >> 2 )& 0x01
        PSH=(flags >> 3 ) & 0x01
        ACK=(flags >> 4 ) & 0x01
        URG=(flags >> 5 ) & 0x01
        WindowSize=tcp[7]
        checksum=tcp[8]
        urgentPointer=tcp[9]


        if sourcePort<1024:
            serverIP=sourceIP
            clientIP=destIP
            serverPort=sourcePort
        elif destPort<1024:
            serverPort=destPort
            clientIP=sourcePort
            serverIP=destIP
        else:
            serverPort="Filtered"
            clientIP="Filtered"
            serverIP="Filtered"

        return (["server IP:"+ serverIP,"client IP:"+clientIP,"Port:"+ serverPort])




    if Upper_protocol==PROTO_UDP:
        udp=unpack('!HHHH',Upper_protocol)

        sourcePort=udp[0]
        destPort=udp[1]
        length=udp[2]
        checksum=udp[3]

        if sourcePort<1024:
            serverIP=sourceIP
            serverPort=sourcePort
            clientIP=destIP
        elif destPort<1024:
            serverIP=destIP
            serverPort=destPort
            clientIP=sourceIP
        else:
            serverPort="Filtered"
            clientIP="Filtered"
            serverIP="Filtered"

        return (["server IP:"+serverIP,"client IP:"+clientIP," Port:"+serverPort])