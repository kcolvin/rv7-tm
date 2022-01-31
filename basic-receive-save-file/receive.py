# Main infinite loop program to ingest UDP messages from RV-7 data radio.
# The data messages arrive via a UDP message on ports 20003 and 20004
# You can read about UDP communications here:
#           https://wiki.python.org/moin/UdpCommunication
#
# The Dynon sends 3 seprate messages over the radio:
# On port 20003, ADAHRS and EMS, alternating every .0625 seconds. They look like this:
#      ADAHRS: !1122054814+019+00051230000+00306-003+01+1099+002+180000230+00739XXXXX22
#      EMS: !3222054815069+04011231123138029029060067069094144XXX+1020506004721XXXXXXXX....
# On port 20004, GPS about every 1 second. Those lines look like this:
#      GPS: $GPRMC,220527.00,A,3514.308512,N,12038.724165,W,9.5,124.7,301221,14.4,E,A*1C
#
# You can decode these lines using the 'DynonDataFormat.pdf' file from the github repo
#
# This program records the data in a raw format into a local .txt file
# with a filename built from the datetime stamp when it starts.
# 
import socket
import datetime
import time
import select
#
# Setup Data UDP socket to listen to port 20003 from anyhost
UDP_PORT = 20003
data_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
data_sock.bind(('',UDP_PORT))
# Setup GPS UDP socket to listen to port 20004 from anyhost
UDP_PORT = 20004
gps_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
gps_sock.bind(('',UDP_PORT))
#
# Initialize file to record raw data
filename = time.strftime("%Y-%m-%d-%H%M%S"+".txt")
print('Filename:',filename)
f = open(filename, "x")
#
# For terminal window:
print('Init complete, listening....')
print('Press CTRL-Break keys to exit.')
#
# infinite loop to process incoming UDP messages
while True:
    # Wait for next Dynon message, then process it
    data, addr = data_sock.recvfrom(1024) # buffer size is 1024 bytes
    adahrs_raw = bytes.decode(data)
    # Write raw data to file
    f.write(adahrs_raw)
    # Acknowledge write to file for testing purposes
    print('Wrote to file:',adahrs_raw)
    # Check for valid ADAHRS message ('!1')
    if (adahrs_raw[1] == '1'):
        # Now get the next msg, which will be an EMS msg
        data, addr = data_sock.recvfrom(1024) # buffer size is 1024 bytes
        ems_raw = bytes.decode(data)
        # Write raw data to file
        f.write(ems_raw)
        # Acknowledge write to file for testing purposes
        print('Wrote to file:',ems_raw)

    # This code quickly checks the GPS socket for data 
    new_gps_data, _, _ = select.select([gps_sock],[],[],.025) #.025 is the timeout (time to wait)
    # If there is data , then process it
    if new_gps_data:
        data = gps_sock.recv(1024)
        gps_raw = bytes.decode(data)
        # write the byte array to the data file
        f.write(gps_raw)
        #
        # Parse the gps message and break into independent variables. 
        # This is only as an example of how to parse the incoming data.
        # Convert the raw data into a list of values
        gps_lst = gps_raw.split(",")
        # This is the NMEA RMC sentence: https://www.trimble.com/OEM_ReceiverHelp/V4.44/en/NMEA-0183messages_RMC.html 
        # Need to reformat NMEA to decimal degrees
        lat = float(gps_lst[3][0:2])+(float(gps_lst[3][2:])/60) # 3514.123093 ddmm.mmmmmm
        lon = -1*(float(gps_lst[5][0:3])+(float(gps_lst[5][3:])/60)) # 12038.044681 dddmm.mmmmmm
        # Truncate to 6 decmial places
        lat = float(f"{lat:.6f}")
        lon = float(f"{lon:.6f}")
        # get other GPS parameters
        gspd = float(gps_lst[7]) # ground track in kts
        #gtrk = float(gps_lst[8]) # ground track in degrees (not needed)
        magvar = float(gps_lst[10]) # magnetic variation in degrees
        # Print GPS data to terminal screen for testing purposes
        print('GPS lat:',lat,'lon:',lon,'gspd',gspd,'magvar',magvar,'\n')