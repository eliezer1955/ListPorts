import cv2
import os
from subprocess import PIPE, run

camera_name = "Arducam OV9281 USB Camera"
cmd ="C:\\Users\\S2\\Downloads\\ffmpeg-6.1.1-essentials_build\\ffmpeg-6.1.1-essentials_build\\bin\\ffmpeg.exe"
command = [cmd,'-f', 'dshow','-list_devices','true','-i','dummy']
result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
print("\r\n\r\n")
for line in result.stderr.splitlines(True):
	print(line)

cam_id = 0

for item in result.stderr.splitlines():
    if camera_name in item:
        cam_id = int(item.split("[")[2].split(']')[0])
print("cam id", cam_id)

cap = cv2.VideoCapture(cam_id)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
ret_val , cap_for_exposure = cap.read()
