# rv7-tm
RV7 telemetry:
To get started, clone this repo and look at code inside the /basic-receive-save-file/ directory.

This was last tested on python 3.9.9, but any Python version 3 should work.

Run the receive.py file at the terminal prompt:
```
python ./receive.py 
```
This will listen for the messages sent from the RV-7 data radio. When it receives messages, it saves the data to a text file.

You can simulate sending data from the RV-7 radio by running the send.py file at another terminal prompt:
```
python ./send.py
```
This will read a testdata.txt file and send those lines via UDP to the receive.py program. This is exactly how the data radio
sends data.

The current goal is to accept the incoming data from the RV-7 radio during flights and visualize it similar to IADS so students can watch the flight in real time:
  
  
![IADS screenshot](https://www.curtisswrightds.com/content/images/IADS-RTStation.png)
