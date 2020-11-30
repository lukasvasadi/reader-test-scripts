import os
import sys
import time
import serial
import platform

from serial.tools import list_ports


# Establish serial connection
def main():
    microcontroller = serial.Serial()
    # Automatically connect to microcontroller
    try:
        port = ""  # Initialize port
        ports_available = list(list_ports.comports())
        if platform.system() == "Windows":
            for com in ports_available:
                if "USB Serial Device" in com.description:
                    port = com[0]
        elif platform.system() == "Darwin" or "Linux":
            for com in ports_available:
                if "USB Serial Device" in com.description:
                    port = com[0]

        print("Port:", port)

        # Open microcontroller on comport
        microcontroller.port = port
        microcontroller.baudrate = 230400
        microcontroller.timeout = 1
        microcontroller.open()

    except AttributeError:
        err = "Error: Problem with serial connection"
        print(err)

    time.sleep(1)

    # Print data
    while True:
        print(microcontroller.readline()[0:-2].decode('utf-8'))
        time.sleep(0.1)

        


if __name__ == '__main__':
    main()
