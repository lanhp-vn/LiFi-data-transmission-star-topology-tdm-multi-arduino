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

# Access parameters from the configuration file
port = config.get('param', 'transmit_port')      # Serial port for transmission
baud_rate = config.getint('param', 'baud_rate')  # Baud rate for serial communication
print(f'Baud rate: {baud_rate}')
no_bit_read = config.getint('param', 'no_bit_read')  # Number of bits to read from the file at once
output_folder = config.get('param', 'output_folder')  # Folder where output files are stored
input_file_name = config.get('param', 'input_file_name')  # Name of the input file
file_type = config.get('param', 'file_type')  # Type of the file (extension)
time_delay = config.getfloat('param', 'time_delay')  # Delay for transmitting

# Construct the full path to the input file
input_file = f'./{output_folder}/{input_file_name}.{file_type}'

# Read the input file and calculate the file size in bits
with open(input_file, 'rb') as file:
    file_content = file.read()
total_bits = len(file_content)  # Calculate total bits (8 bits per byte)
print(f'File size: {total_bits} bits')

# Initialize serial communication with the specified port and baud rate
with serial.Serial(port, baud_rate) as arduino:
    # Wait for 2 seconds to allow the connection to initialize
    time.sleep(2)

    # Open the output file in binary mode for transmission
    with open(input_file, 'rb') as file:
        while True:
            byte = file.read(no_bit_read)  # Read a byte from the file
            if not byte:  # If no byte is read (end of file), exit the loop
                arduino.write('++END++'.encode('utf-8'))
                break
            # Send the byte to the Arduino via serial port
            arduino.write(byte)
            # Wait for a short period to prevent buffer overflow and ensure data integrity
            time.sleep(time_delay)

# Ensure the serial connection is closed after the operation
arduino.close()
