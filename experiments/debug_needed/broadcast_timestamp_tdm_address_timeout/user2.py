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
user_id = 2
user_receive = 3
transmit_id = f"TX{user_id}"
receive_id = f"RX{user_receive}"
address = transmit_id + receive_id

port = config.get('param', f'user{user_id}_port')      # Serial port
no_active_users = config.getint('param', 'no_active_users')   # Including users + 1 router

baud_rate = config.getint('param', 'baud_rate')  # Baud rate for serial communication

endSignal_message = config.get('param', 'endSignal_message')     # End signal after users finish their message
endSignal_timeslot = config.get('param', 'endSignal_timeslot')   # End signal after users finish their turn
endSignal_router = config.get('param', 'endSignal_router')   # End signal after router finishes its turn
endSignal_all = endSignal_message + endSignal_message + endSignal_router
timestamp = config.get('param', 'timestamp')

timeslot_duration = config.getfloat('param', 'timeslot_duration')   # Timeslot duration assigned to each user not including guard band
guard_band = config.getfloat('param', 'guard_band')  # To prevent interference between time slots
interval = (timeslot_duration + guard_band) * no_active_users    # Interval at which users finish transmitting (milliseconds)
transmit_time = timeslot_duration + guard_band

no_bit_read = config.getint('param', 'no_bit_read')  # Number of bits to read from the file at once
receive_wait_time = interval * 3

input_file_name = config.get('param', f'user{user_id}_input_file')  # Name of the input file
file_type = config.get('param', 'file_type')  # Type of the file
output_folder = config.get('param', 'output_folder')  # Folder where output files are stored

# Construct the full path to the input file
input_file = f'./{output_folder}/{input_file_name}.{file_type}'
file_size = os.path.getsize(input_file)

# Construct the full path to the output file
output_file_name = f'router_received.{file_type}'
output_file = f'./{output_folder}/{output_file_name}'

first_loop = True
isTransmitting = False
file_end = False

# Initialize serial communication with the specified port and baud rate
with serial.Serial(port, baud_rate) as arduino:

    while not arduino.isOpen():
        pass

    with open(input_file, 'rb') as file:

        while arduino.isOpen():

            print("Arduino opened")

            check_fileSize = 0

            while first_loop:
                if arduino.in_waiting:
                    data = arduino.read(arduino.in_waiting)
                    print(f"data: {data}")
                    buffer += data
                    # Check if timestamp is detected
                    if buffer.endswith(timestamp.encode('utf-8')):
                        print(f"Timestamp detected, user{user_id} starts")
                        buffer = b""
                        first_loop = False
                        isTransmitting = True

            ### TRANSMITTING
            if not first_loop:
                start_time = time.time()  # Get the current time in seconds
                isTransmitting = True
                toAttachID = 0
                endTimeslot = True

            while isTransmitting:
                elapsed_time = time.time() - start_time
                # print(f"elapsed time: {elapsed_time:.2f}")

                if not file_end and transmit_time * (user_id - 1) <= elapsed_time <= transmit_time * (user_id - 1) + timeslot_duration:

                    if toAttachID == 0:
                        arduino.write(address.encode('utf-8'))

                    data = file.read(no_bit_read)  # Read a byte from the file
                    if check_fileSize > file_size:  # If no byte is read (end of file), exit the loop
                        arduino.write(endSignal_message.encode('utf-8'))
                        arduino.write(endSignal_timeslot.encode('utf-8'))
                        print(f"end of file user{user_id}")
                        # isTransmitting = False
                        file_end = True
                    else:
                        arduino.write(data)
                        check_fileSize += no_bit_read
                        print(data)

                    toAttachID += 1

                if not file_end and transmit_time * (user_id - 1) + timeslot_duration < elapsed_time <= transmit_time * user_id:
                    if endTimeslot == True:
                        arduino.write(endSignal_timeslot.encode('utf-8'))
                    endTimeslot = False
                
                if file_end or interval - transmit_time < elapsed_time <= interval:
                    if arduino.in_waiting:
                        data = arduino.read(arduino.in_waiting)
                        buffer += data
                        if buffer.endswith(endSignal_all.encode('utf-8')):
                            arduino.close()
                            isTransmitting = False
                            break
                    isTransmitting = False
                    


with open(output_file, 'wb') as f:
    f.write(buffer)