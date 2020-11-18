import os
import sys
import time
import serial
import platform

from serial.tools import list_ports


def connect():
    reader0 = serial.Serial()
    reader1 = serial.Serial()
    # Automatically connect to readers
    try:
        ports = []  # Initialize port list
        ports_available = list(list_ports.comports())
        if platform.system() == "Windows":
            for com in ports_available:
                if "USB Serial Port" in com.description:
                    ports.append(com[0])
        elif platform.system() == "Darwin" or "Linux":
            for com in ports_available:
                if "FT232R USB UART" in com.description:
                    ports.append(com[0])

        print("Ports:", ports[0], ports[1])

        # Update comport setup data
        reader0.port = ports[0]
        reader0.baudrate = 500000
        reader0.timeout = 1

        reader1.port = ports[1]
        reader1.baudrate = 500000
        reader1.timeout = 1

        # Open both readers
        reader0.open()
        reader1.open()

        readers = (reader0, reader1)
        print(readers)

        # Reset microcontroller
        for reader in readers:
            reader.setDTR(False)
            time.sleep(0.1)
            # Wipe serial buffers
            reader.reset_input_buffer()
            reader.reset_output_buffer()
            reader.setDTR(True)
        
        return readers

    except AttributeError:
        err = "Error: Problem with serial connection"
        print(err)


def setup(readers):
    setting = input("Setting ('c' or 's'): ")
    median = input("Median: ")

    if setting == 's':
        amplitude = input("Amplitude: ")
        frequency = input("Frequency: ")
    else:
        amplitude = '0'
        frequency = '0'
    
    debug = input("Debug ('0' or '1'): ")

    setup_commands = '<' + setting + ';' + median + ';' + amplitude + ';' + frequency + ';' + debug + '>'
    print("Setup:", setup_commands)

    for reader in readers:
        reader.write(setup_commands.encode())


# Establish serial connection
def main():
    # Connect readers
    readers = connect()
    # Package and send setup commands
    setup(readers)

    time.sleep(2)

    # Print data
    while True:
        data0 = readers[0].readline()[0:-2].decode('utf-8')
        data1 = readers[1].readline()[0:-2].decode('utf-8')
        print(data0, data1)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
