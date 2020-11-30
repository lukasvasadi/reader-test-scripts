import os
import sys
import time
import serial
import platform

from serial.tools import list_ports


# Bundle setup commands into readable format
def package_setup_commands():
    setting = input("Setting ('c' or 's'): ")
    median = input("Median: ")
    debug = input("Debug ('1' or '0'): ")
    
    if setting == 's':
        amplitude = input("Amplitude: ")
        frequency = input("Frequency: ")
    else:
        amplitude = '0'
        frequency = '0'

    setup_commands = '<' + setting + ';' + median + ';' + amplitude + ';' + frequency + ';' + debug + '>'
    print("Setup:", setup_commands)
    return setup_commands


# Establish serial connection
def main():
    reader = serial.Serial()
    # Automatically connect to reader
    try:
        port = ""  # Initialize port
        ports_available = list(list_ports.comports())
        if platform.system() == "Windows":
            for com in ports_available:
                if "USB Serial Port" in com.description:
                    port = com[0]
        elif platform.system() == "Darwin" or "Linux":
            for com in ports_available:
                if "FT232R USB UART" in com.description:
                    port = com[0]

        print("Port:", port)

        # Open reader on comport
        reader.port = port
        reader.baudrate = 500000
        reader.timeout = 1
        reader.open()

        # Reset microcontroller
        reader.setDTR(False)
        time.sleep(0.1)
        # Wipe serial buffers
        reader.reset_input_buffer()
        reader.reset_output_buffer()
        reader.setDTR(True)

    except AttributeError:
        err = "Error: Problem with serial connection"
        print(err)
    
    # Package and send setup commands
    setup_commands = package_setup_commands()
    reader.write(setup_commands.encode())

    time.sleep(1)

    # Print data
    while True:
        print(reader.readline()[0:-2].decode('utf-8'))
        time.sleep(1)


if __name__ == '__main__':
    main()
