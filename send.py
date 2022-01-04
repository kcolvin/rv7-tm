# Read file, then send UDP messages spaced 62.5 milliseconds apart (16 Hz)
import socket
import time
# Setup UDP
UDP_IP = "44.239.172.205"  # This is the Elastic IP of the IoT Server in the IME AWS acct.
#UDP_IP = "localhost"
UDP_PORT = 20003
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
# This is the send command, use it in the loop below
#sock.sendto(MESSAGE, (UDP_IP, UDP_PORT)) 
# Open test file and send byte arrarys to the IoT server
#with open('test-adahrs.txt', 'r') as f:
#with open('test-both.txt', 'r') as f:
with open('2021-01-05-235659.txt', 'r') as f:
    for line in f:
        print(str.encode(line))
        sock.sendto(str.encode(line), (UDP_IP, UDP_PORT)) # Send as a byte array instead of string
        time.sleep(.0625)
        # process a line at a time
f.close() 
