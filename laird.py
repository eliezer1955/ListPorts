import serial
import json
import serial.tools.list_ports
import time
import sys

portName = ""
global thermoPort

def findLaird():
    ports={}
    fileName="c:\ProgramData\LabScript\Data\comports.json"
    with open(fileName,'r') as jfile:
        dataJson=jfile.read()
        ports=json.loads(dataJson)
    portsNow = serial.tools.list_ports.comports()
    for p in portsNow:
        if p.device in ports.values():
            portName=""
            continue
        else:
            portName=p.device
        if portName == "":
            print("Cannot find Laird device")
            sys.exit(255)
        else:
            print("Potential Laird found at "+portName)
        thermoPort=serial.Serial(portName,115200,timeout=0.2)                  
        thermoPort.write(b"$v\r\n");
        time.sleep(.1)
        response = thermoPort.readline()
        response = thermoPort.readline()
        if b"SC_v" in response:
            print("Laird found at "+thermoPort.name)
            break
        else:
            portName=""
            thermoPort.close()
    if thermoPort.is_open:
        thermoPort.write(b"$A0\r\n")
        response=thermoPort.readline()
    return thermoPort

def ReadTemp():
    thermoPort.write(b"$R100?\r\n")
    response = thermoPort.readline()
    if response==b"\r\n":
        response = thermoPort.readline()
    response=thermoPort.readline()
    return response.decode().strip()


thermoPort=findLaird()
startTime=time.time()
print(thermoPort)
while True:
    temp=ReadTemp()
    if temp == ">" :
        continue;
    ct=time.time()-startTime
    print(ct, float(temp))
    time.sleep(0.5)
