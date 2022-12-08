from socket import *

#Build and send the IP offer
def buildPacket(CL_HLEN, CL_XID, CL_CHADDR, IP_POOL, pk_type)
    
    print("Recieved packet, type: ", pk_type)
    
    #need to build and send offer
    OP = [0x02]
    HTYPE = [0x01]
    HLEN = [0x06]
    HOPS = [0x00]
    XID = [hex(CL_XID)] #Client generated transaction number
    SECS = [0x00, 0x00]
    FLAGS = [0x00, 0x00]
    CIADDR = [0x00, 0x00, 0x00, 0x00]
    
    # If it is a discovery message, find new IP address. Else, find the stored IP (unknown if works)
    if pk_type == 0:
        for c in range(2,254):
            tempIP = [0xC0, 0xA8, 0x00, hex(c)]
            if tempIP not in IP_POOL.values :
                YIADDR = tempIP
                IP_POOL[CL_CHADDR] = tempIP
                break
    else:
        YIADDR = IP_POOL.get(CL_CHADDR)
    
    
    YIADDR = [0xC0, 0xA8, 0x00, newEnd] #client ip offer
    SIADDR = [0xC0, 0xA8, 0x00, 0x01] #Server IP 192.168.0.1
    GIADDR = [0x00, 0x00, 0x00, 0x00]
    CHADDR = [hex(CL_CHADDR)] #Client mac address: 6 bytes
    
    #Pad the MAC address with zeroes
    #CHADDR_PAD = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    CHADDR_DIFF = hex(CL_HLEN)
    CHADDR_PAD = []
    for i in range(CHADDR_DIFF):
        CHADDR_PAD.append([0x00])
        
    #Add the sname and file, fill with zeros
    SN_FILE = []
    for j in range(192):
        SN_File.append([0x00])
    
    #The rest or the stuffs
    MagicCookie = [0x63, 0x82, 0x53, 0x63]
    if pk_type == 0:
        OPTION1 = [0x35, 0x01, 0x02] #53, 1, 2 = DCHP offer
    else:
        OPTION1 = [0x35, 0x01, 0x05] #53, 1, 5 = DCHP ACK
    #OPTION2 = bytes([0x01, 0x04, 0xFF, 0xFF, 0xFF, 0x00]) #1, 4 = subnet mask, set to 255.255.255.0 for now
    OPTION3 = [0x33, 0x04, 0x00, 0x01, 0x51, 0x80] # Lease time of one day, in seconds
    
    packet = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR + YIADDR + SIADDR + GIADDR + CHADDR + CHADDR_PAD + SN_FILE + MagicCookie + OPTION1 + OPTION3
    
    return bytes(packet)







DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)

#addrPool = [ 2, 3, 4, 5, 6, 7, 8, 9, 10 ] #pool of addresses, stored as the last byte ( 192.168.0.X )
#addrUsed = [ false, false, false, false, false, false, false, false, false ] #Keeps track of used addresses #Replace with mac addresses  

# Pool of ip's idea: run a for loop from 1 to 254 for new ip's, store the used ip's somehow.



# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

# IP address storage pool
IP_POOL = {}

# Server loop
while 1:
    # Recieving Broadcast
    msg, addr = s.recvfrom(1024)
    
    #need to parse recieved packet
    CL_OP = msg[0:1] #1 Byte, 1 request, 2 reply 
    CL_HTYPE = msg[1:2] #1 Byte, type of HW, 1 for ethernet
    CL_HLEN =  msg[2:3]#1 Byte, number of bytes used for mac addr, usually 6
    CL_HOPS = msg[3:4]#1 Byte, number of relays the message has passed through
    CL_XID = msg[4:8]#4 Byte, transaction ID determined by client
    CL_SECS = msg[8:10]:#2 Byte, # of seconds since request started 
    CL_FLAGS = msg[10:12]#2 Byte, look it up
    CL_CIADDR = msg[12:16]#4 Byte, IP of client
    CL_YIADDR = msg[16:20]#4 Byte, IP for client offer, filled in offer and ACK
    CL_SIADDR = msg[20:24]#4 Byte, IP of DHCP server, filled in offer and ACK
    CL_GIADDR = msg[24:28]#4 Byte, IP of DHCP server, filled in offer and ACK
    CL_CHADDR = msg[28:34]#16 Byte client mac address 

    """
    CL_MagicCookie = 
    CL_DHCPOP1 = 
    CL_DHCPOP2 = 
    CL_DHCPOP3 = 
    CL_DHCPOP4 = 
    """
    
    if CL_CHADDR in IP_POOL:
        packet = buildPacket(CL_HLEN, CL_XID, CL_CHADDR, IP_POOL, 1) #Sending ACK
    else:
        packet = buildPacket(CL_HLEN, CL_XID, CL_CHADDR, IP_POOL, 0) #Send Offer
   
    #Send the packet to the client
    s.sendto(packet, DHCP_CLIENT)
    
    
    """
    #Need to find IP from pool to offer
    for x in range(len(addrUsed)):
        if addrUsed[x] == false:
            newEnd = hex(addrPool[x]) #Unused address end as hex value
            poolLocation = x          #Used to mark the IP as in use, after the client accepts
            break
    
    #need to build and send offer
    OP = bytes([0x02])
    HTYPE = bytes([0x01])
    HLEN = bytes([0x06])
    HOPS = bytes([0x00])
    XID = CL_XID #Client generated transaction number
    SECS = bytes([0x00, 0x00])
    FLAGS = bytes([0x00, 0x00])
    CIADDR = bytes([0x00, 0x00, 0x00, 0x00])
    YIADDR = bytes([0xC0, 0xA8, 0x00, newEnd]) #client ip offer
    SIADDR = bytes([0xC0, 0xA8, 0x00, 0x01]) #Server IP 192.168.0.1
    GIADDR = bytes([0x00, 0x00, 0x00, 0x00])
    CHADDR = CL_CHADDR #Client mac address: Pad with lots of zeroes
    
    MagicCookie = bytes([0x63, 0x82, 0x53, 0x63])
    OPTION1 = bytes([0x35, 0x01, 0x02]) #53, 1, 2 = DCHP offer
    OPTION2 = bytes([0x01, 0x04, 0xFF, 0xFF, 0xFF, 0x00]) #1, 4 = subnet mask, set to 255.255.255.0 for now
    OPTION3 = bytes([0x33, 0x04, 0x00, 0x01, 0x51, 0x80]) # Lease time of one day, in seconds
    
    packet = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR + YIADDR + SIADDR + GIADDR + CHADDR + MagicCookie + OPTION1 + OPTION2 + OPTION3
    
    s.sendto(packet, DHCP_CLIENT)
    
    #while loop, need to wait for request response
    #acknowledge request response
    """









"""
# Recieve a UDP message
msg, addr = s.recvfrom(1024)

# Print the client's MAC Address from the DHCP header
print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
for i in range(29, 34):
	print(":" + format(msg[i], 'x'), end = '')
print()

# Send a UDP message (Broadcast)
s.sendto(b'Hello World!', DHCP_CLIENT)

"""
