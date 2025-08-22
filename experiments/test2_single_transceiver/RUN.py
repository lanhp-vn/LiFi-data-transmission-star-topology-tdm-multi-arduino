import multiprocessing
import configparser
import subprocess
import re

# Initialize the parser
config = configparser.ConfigParser()

# Read the config file
config.read('config.ini')

input_file_name = config.get('param', 'input_file_name')
output_folder = config.get('param', 'output_folder')
file_type = config.get('param', 'file_type')

transmit_port = config.get('param', 'transmit_port')  # Serial port for transmission
receive_port = config.get('param', 'receive_port')  # Serial port for reception
router_port = config.get('param', 'router_port')  # Serial port for reception

baudrate = config.getint('param', 'baud_rate')  # Baud rate for serial communication

transmit_path = config.get('param', 'transmit_path')  # Path to transmit sketch
receive_path = config.get('param', 'receive_path')  # Path to receive sketch
router_path = config.get('param', 'router_path')  # Path to receive sketch

transmit_script = 'main_transmit.py'
receive_script = 'main_receive.py'

def set_baudrate(file_path, baudrate):
    with open(file_path, 'r+') as file:
        content = file.read()
        content_new = re.sub(r'(const unsigned long baudrate = )(\d+)(;)', r'\g<1>{}\g<3>'.format(baudrate), content)
        file.seek(0)
        file.write(content_new)
        file.truncate()

def upload_to_arduino(file_path, port):
    cmd = f'arduino-cli compile --upload --port {port} --fqbn arduino:avr:uno {file_path}'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.stdout.read().decode())

def run_script1():
    exec(open(transmit_script).read())

def run_script2():
    exec(open(receive_script).read())

def calculate_ber(transmitting_file, receiving_file):
    # Read both files in binary mode
    with open(transmitting_file, 'rb') as file1, open(receiving_file, 'rb') as file2:
        file1_content = file1.read()
        file2_content = file2.read()

    # Find the length of the shorter file
    min_len = min(len(file1_content), len(file2_content))

    # Count the number of differing bits
    error_count = sum(bin(byte1 ^ byte2).count('1') for byte1, byte2 in zip(file1_content[:min_len], file2_content[:min_len]))

    # Add the rest of the bits from the longer file, if lengths are unequal
    if len(file1_content) > len(file2_content):
        error_count += sum(bin(byte).count('1') for byte in file1_content[min_len:])
    else:
        error_count += sum(bin(byte).count('1') for byte in file2_content[min_len:])

    # Calculate the total number of bits
    total_bits = 8 * max(len(file1_content), len(file2_content))
    # total_bits = max(len(file1_content), len(file2_content))

    # Calculate the BER
    ber = error_count / total_bits

    return ber, error_count, total_bits

if __name__ == '__main__':

    # Set baudrate for Arduino
    set_baudrate(transmit_path, baudrate)
    set_baudrate(receive_path, baudrate)
    set_baudrate(router_path, baudrate)

    # Upload to Arduino
    upload_to_arduino(router_path, router_port)
    upload_to_arduino(transmit_path, transmit_port)
    upload_to_arduino(receive_path, receive_port)

    print("Successfully uploading sketches to Arduino!")

    # Create two processes
    process1 = multiprocessing.Process(target=run_script1)
    process2 = multiprocessing.Process(target=run_script2)

    # Start the processes
    process1.start()
    process2.start()

    # Wait for all processes to finish
    process1.join()
    process2.join()

    transmit_file = f'./{output_folder}/{input_file_name}_transmit_data.bin'
    receive_file = f'./{output_folder}/{input_file_name}_received_data.bin'
    transmit_file = f'./{output_folder}/{input_file_name}.{file_type}'
    receive_file = f'./{output_folder}/{input_file_name}_received_data.{file_type}'

    # Calculate BER of the link
    ber, error_count, total_bits = calculate_ber(transmit_file, receive_file)
    print(f"Bit Error Rate (BER): {ber}")
    print(f"Total number of errors: {error_count}")