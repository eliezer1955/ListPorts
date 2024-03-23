import serial
import json
import serial.tools.list_ports
import time
import sys

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

global fig
global ys
global ax
global xs
global allx, ally
global startTime
allx = []
ally = []
xs = []
ys = []


def startplot():
    # Create figure for plotting
    global fig, xs, ys, ax, allx, ally, startTime
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    allx = []
    ally = []
    return fig, xs, ys, allx, ally


portName = ""
global thermoPort


def findLaird():
    global thermoPort
    ports = {}
    fileName = "c:\ProgramData\LabScript\Data\comports.json"
    with open(fileName, 'r') as jfile:
        dataJson = jfile.read()
        ports = json.loads(dataJson)
    portsNow = serial.tools.list_ports.comports()
    for p in portsNow:
        if p.device in ports.values():
            portName = ""
            continue
        else:
            portName = p.device
        if portName == "":
            print("Cannot find Laird device")
            sys.exit(255)
        else:
            print("Potential Laird found at "+portName)
        thermoPort = serial.Serial(portName, 115200, timeout=0.2)
        thermoPort.write(b"$v\r\n")
        time.sleep(.1)
        response = thermoPort.readline()
        response = thermoPort.readline()
        if b"SC_v" in response:
            print("Laird found at "+thermoPort.name)
            break
        else:
            portName = ""
            thermoPort.close()
    if thermoPort.is_open:
        thermoPort.write(b"$A0\r\n")
        response = thermoPort.readline()
    return thermoPort


def ReadTemp():
    global thermoPort
    thermoPort.write(b"$R100?\r\n")
    response = thermoPort.readline()
    if response == b"\r\n":
        response = thermoPort.readline()
    response = thermoPort.readline()
    return response.decode().strip()


def run_animation():
    global thermoPort, startTime, allx, ally
    
# This function is called periodically from FuncAnimation

    def animate(i, xs, ys, allx, ally):
        global fig, ax, startTime
        # Read temperature (Celsius) from TMP102
        t = float(ReadTemp())
        temp_c = round(t, 2)

        # Add x and y to lists
        now = (dt.datetime.now()-startTime).total_seconds()
        xs.append(now)
        ys.append(temp_c)
        allx.append(now)
        ally.append(temp_c)

        # Limit x and y lists to 100 items
        xs = xs[-100:]
        ys = ys[-100:]

        # Draw x and y lists
        ax.clear()
        ax.plot(xs, ys)

        # Format plot
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Laird Temperature over Time')
        plt.ylabel('Temperature (deg C)')
        plt.xlabel('Time (s)')


    def onClick(event):
        nonlocal anim_running
        if anim_running:
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True

    anim_running = True
    
    startTime = dt.datetime.now()
    fig.canvas.mpl_connect('button_press_event', onClick)
    # Set up plot to call animate() function periodically
    anim = animation.FuncAnimation(fig, animate, fargs=(xs, ys, allx, ally),
                                   interval=1000, cache_frame_data=False)
    plt.show()

    
thermoPort = findLaird()
print(thermoPort)
fig, xs, ys, allx, ally = startplot()
run_animation()
# Show summary plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# Draw x and y lists
ax.plot(allx, ally)
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
plt.title('Laird Temperature over Time')
plt.ylabel('Temperature (deg C)')
plt.xlabel('Time (s)')
plt.show()
# save plot to disk
plt.savefig("lairdTemp.png")
