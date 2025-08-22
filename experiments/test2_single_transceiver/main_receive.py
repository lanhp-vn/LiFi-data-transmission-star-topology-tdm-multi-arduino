import serial
import os
import time
import configparser

# Initialize the parser for reading the configuration file
config = configparser.ConfigParser()

# Read the configuration from 'config.ini'
config.read('config.ini')

# Access parameters from the configuration file
port = config.get('param', 'receive_port')               # Serial port for receiving data
baud_rate = config.getint('param', 'baud_rate')          # Baud rate for serial communication
receive_wait_time = config.getint('param', 'receive_wait_time')  # Timeout for receiving data
output_folder = config.get('param', 'output_folder')     # Folder where received files will be stored
input_file_name = config.get('param', 'input_file_name') # Base name for the input file
file_type = config.get('param', 'file_type')             # File type/extension of the received file

# Construct the output file name and path
output_file_name = f'{input_file_name}_received_data.{file_type}'
output_file = f'./{output_folder}/{output_file_name}'

# Record the last time data was received to determine timeout
last_receive = time.time()
# Variable to keep track of the current time
current_time = time.time()

# Establish a connection to the serial port with the specified parameters
with serial.Serial(port, baud_rate) as arduino:
    # Allow time for the serial connection to establish
    time.sleep(1)
    
    # Wait until there is data waiting in the serial buffer
    while not arduino.in_waiting:
        pass
    
    # Open the output file in binary write mode
    with open(output_file, 'wb') as f:
        # Continuously read and save data from the serial port
        while True:
            # Check if there is data in the serial buffer
            if arduino.in_waiting:
                # Read all the data waiting in the buffer
                data = arduino.read(arduino.in_waiting)
                print(data)
                # Write the data to the file
                f.write(data)
                # Update the last received time
                last_receive = current_time
            # If the current time exceeds the last receive time by the wait threshold, exit the loop
            elif current_time - last_receive > receive_wait_time: 
                break
            # Update the current time
            current_time = time.time()