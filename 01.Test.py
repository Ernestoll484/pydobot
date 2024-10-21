from serial.tools import list_ports
from pydobot import Dobot
from time import sleep

for c in list_ports.comports():
    print(c.device)

portDoBot = list_ports.comports()[0].device # /dev/cu.SLAB_USBtoUART
device = Dobot(port=portDoBot)

while True:
    x, y, z, r, j1, j2, j3, j4 = device.pose()
    print(f"x={x:9.4f}, y={y:9.4f}, z={z:9.4f}, r={r:9.4f}, j1={j1:9.4f}, j2={j2:9.4f}, j3={j3:9.4f}, j4={j4:9.4f}")
    sleep(0.2)
    
device.close()