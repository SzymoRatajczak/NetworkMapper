import socket
import os
import sys
from struct import *

PROTOCOL_TCP=6

def PacketExtractor(packet):
    striped_packet=packet[0:20]
    unpacked_tuple=unpack('!BBHHHBBH4s4s',striped_packet)

    version_HeaderLen=unpacked_tuple[0]
    TOS=unpacked_tuple[1]
    Entire_length=unpacked_tuple[2]
    ID=unpacked_tuple[3]
    flags=unpacked_tuple[4]
    RES=(flags >>15) & 0x01 #reserverd
    DF=(flags >> 14) &0x01 #do not fragment
    MF=(flags >>13) & 0x01 #more fragment
    TTL=unpacked_tuple[5]
    Upper_Protocol=unpacked_tuple[6]
    checksum=unpacked_tuple[7]
    sourceIP=unpacked_tuple[8]
    destIP=unpacked_tuple[9]

    version=version_HeaderLen >> 4
    length= version_HeaderLen >> 0x0F
    ipHeaderlength=length * 4

    #conversion of IP addresses into a doted notation

    sourceIP=socket.inet_ntoa(sourceIP)
    destinationIP=socket.inet_ntoa(destIP)

    if Upper_Protocol==PROTOCOL_TCP:
        stripTCPHeader=packet[ipHeaderlength:ipHeaderlength+20]

        tcpHeaderBuffer=unpack('!HHLLBBHHH',stripTCPHeader)

        sourcePort=tcpHeaderBuffer[0]
        destinationPort=tcpHeaderBuffer[1]
        sequenceNumber=tcpHeaderBuffer[2]
        acknowledgeNumber=tcpHeaderBuffer[3]
        reserver=tcpHeaderBuffer[4]
        headerLength=tcpHeaderBuffer[5]
        flags=tcpHeaderBuffer[6]
        FIN=flags & 0x01
        SYN=(flags >> 1 ) & 0x01
        RST=(flags >> 2) & 0x01
        PSH=(flags >> 3) & 0x01
        ACK=(flags >> 4 ) & 0x01
        URG=(flags >> 5 ) & 0x01
        ECE=(flags >> 6 ) & 0x01
        CWR=(flags >> 7 )& 0x01


        WindowSize=tcpHeaderBuffer[7]
        checksum=tcpHeaderBuffer[8]
        urgentPointer=tcpHeaderBuffer[9]


        if sourcePort<1024:
            serverIP=sourceIP
            clientIP=destinationIP
            serverPort=sourcePort
        elif destinationPort<1024:
            clientIP=sourceIP
            serverIP=destinationIP
            serverPort=destinationPort
        else:
            clientIP="Filter"
            serverIP="filter"
            serverPort="filtered"

        return([serverIP,clientIP,serverPort],[SYN,serverIP,TOS,TTL,DF,WindowSize])

    else:
        return(["Filtered","Filtered","Filtered"],[" " ," ", " "," "])



if __name__=="__main__":

        ret=os.system("ifconfig eth0 promisc")

        if ret==0:
            try:
                sock=socket.socket(socket.AF_INET,socket.SOCK_RAW)

                print("RAW socket open")

            except:
                print("raw socket failed")
                sys.exit()

        ipObservations=[]
        osObservations=[]

        maxObservations=500


        portValue=443

        while maxObservations > 0:
            data,addr=sock.recv(500)
            content,fingerPrint=PacketExtractor(data)

            if content[0]!="Filtered":
                ipObservations.append(content)
                maxObservations-=1
                if fingerPrint[0]==1:
                    osObservations.append(fingerPrint)
                else:
                    continue
            else:
                continue

        print("socket failed")

        print("Capture complete, promiscoue mode can be close ")
        os.system("ifconfig eth0 ~promisc")
        sock.close()

        ipObservations.sort()
        osObservations.sort()

        print("Result of the IP observations:")
        for i in ipObservations:
            print(i)

        print("\n"* 10)

        print("result of the OS observations:")
        for i in osObservations:
            print(i)

















