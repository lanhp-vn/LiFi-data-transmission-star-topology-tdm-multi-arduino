# Import necessary libraries
import serial          # To communicate with serial ports
import time            # To use sleep for timing
import os              # To interact with the operating system
import numpy as np     # For numerical operations (not used in this snippet)
import configparser    # For parsing configuration files

# Initialize the parser for reading the configuration file
config = configparser.ConfigParser()

# Read the configuration from 'config.ini'
config.read('config.ini')

port = config.get('param', f'router_port')      # Serial port
baud_rate = config.getint('param', 'baud_rate')  # Baud rate for serial communication
no_active_users = config.getint('param', 'no_active_users')
timeslot_duration = config.getfloat('param', 'timeslot_duration')   # Timeslot duration assigned to each user not including guard band
guard_band = config.getfloat('param', 'guard_band')  # To prevent interference between time slots
interval = (timeslot_duration + guard_band) * no_active_users    # Interval at which users finish transmitting (milliseconds)

endSignal_timeslot = config.get('param', 'endSignal_timeslot')   # End signal after users finish their turn
endSignal_router = config.get('param', 'endSignal_router')   # End signal after router finishes its turn

receive_wait_time = interval * 4

file_type = config.get('param', 'file_type')  # Type of the file
output_folder = config.get('param', 'output_folder')  # Folder where output files are stored

# Construct the full path to the output file
output_file_name = f'router_received.{file_type}'
output_file = f'./{output_folder}/{output_file_name}'

isReceiving = False

# Initialize serial communication with the specified port and baud rate
with serial.Serial(port, baud_rate) as arduino:

    while not arduino.isOpen():
        pass

    with open(output_file, 'wb') as f:
        last_receive = time.time()  # Initialize the last data received time

        while arduino.isOpen():
            # Check if receive_wait_time have passed without data
            current_time = time.time()
            elapsed_time = current_time - last_receive
            if elapsed_time > receive_wait_time:
                print("Router timeout")
                arduino.close()
                break
            
            ### RECEIVING
            
            # Initialize variables
            buffer = b""

            if arduino.in_waiting:
                isReceiving = True
                last_receive = time.time()  # Update the last data received time

            # Continuously read and process data from the serial port
            while isReceiving:

                if arduino.in_waiting:
                    # Read all the data waiting in the buffer
                    data = arduino.read(arduino.in_waiting)
                    # print(data)
                    
                    # Append the received data to the data buffer
                    buffer += data
                    # print(f"buffer: {buffer}")

                    # Check if endSignal_router is detected
                    if buffer.endswith(endSignal_router.encode('utf-8')):
                        # Remove endSignal_router from the end of buffer
                        buffer = buffer[:-len(endSignal_router.encode('utf-8'))]
                        print("write to file")
                        f.write(buffer)
                        # Clear the data buffer
                        buffer = b""
                        isReceiving = False