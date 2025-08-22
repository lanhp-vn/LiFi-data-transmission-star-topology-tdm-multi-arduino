import multiprocessing
import configparser
import subprocess
import re

# Initialize the parser
config = configparser.ConfigParser()

# Read the config file
config.read('config.ini')

no_active_users = config.getint('param', 'no_active_users')

endSignal_message = config.get('param', 'endSignal_message')     # End signal after users finish their message
endSignal_timeslot = config.get('param', 'endSignal_timeslot')   # End signal after users finish their turn
endSignal_router = config.get('param', 'endSignal_router')       # End signal after router finishes its turn

baud_rate = config.getint('param', 'baud_rate')  # Baud rate for serial communication
timestamp = config.get('param', 'timestamp')

timeslot_duration = config.getfloat('param', 'timeslot_duration')   # Timeslot duration assigned to each user not including guard band
guard_band = config.getfloat('param', 'guard_band')  # To prevent interference between time slots
interval = (timeslot_duration + guard_band) * no_active_users    # Interval at which users + router finish transmitting (milliseconds)

router_port = config.get('param', 'router_port')  # Serial port for router
user_ports = [config.get('param', f'user{i}_port') for i in range(1, no_active_users)] # Serial ports for users

output_folder = config.get('param', 'output_folder')
file_type = config.get('param', 'file_type')

user_path = config.get('param', 'user_path')  # Path to users' Arduino sketch
router_path = config.get('param', 'router_path')  # Path to router's Arduino sketch



def set_variables(file_path, baud_rate, endSignal_timeslot, endSignal_router, timestamp, interval):
    with open(file_path, 'r+') as file:
        content = file.read()
        
        # Modify 'baud_rate' variable
        content = re.sub(r'(const unsigned long baud_rate = )(\d+)(;)', r'\g<1>{}\g<3>'.format(baud_rate), content)

        # Modify 'endSignal_timeslot' variable
        content = re.sub(r'(String endSignal_timeslot = ")(.*)(";)', r'\g<1>{}\g<3>'.format(endSignal_timeslot), content)

        # Modify 'endSignal_router' variable
        content = re.sub(r'(String endSignal_router = ")(.*)(";)', r'\g<1>{}\g<3>'.format(endSignal_router), content)

        # Modify 'interval' variable
        content = re.sub(r'(float interval = )(.+);', r'\g<1>{};'.format(interval), content)

        # Modify 'timestamp' variable
        content = re.sub(r'(String timestamp = ")(.*)(";)', r'\g<1>{}\g<3>'.format(timestamp), content)
        
        file.seek(0)
        file.write(content)
        file.truncate()
        print(f"Variables in {file_path} are updated")

def upload_to_arduino(file_path, port):
    cmd = f'arduino-cli compile --upload --port {port} --fqbn arduino:avr:uno {file_path}'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    # print(process.stdout.read().decode())
    print(f"{file_path} was uploaded to {port}")

def run_script1():
    exec(open('user1.py').read())

def run_script2():
    exec(open('user2.py').read())

def run_script3():
    exec(open('user3.py').read())

def run_script_router():
    exec(open('main_router.py').read())

    
if __name__ == '__main__':

    # Create processes for active users
    process1 = multiprocessing.Process(target=run_script1)
    process2 = multiprocessing.Process(target=run_script2)
    process3 = multiprocessing.Process(target=run_script3)
    process_router = multiprocessing.Process(target=run_script_router)

    # Set variables for Arduino sketches
    set_variables(user_path, baud_rate, endSignal_timeslot, endSignal_router, timestamp, interval)
    set_variables(router_path, baud_rate, endSignal_timeslot, endSignal_router, timestamp, interval)

    # Upload sketches to Arduino for router and active users
    for i in range(no_active_users-1):
        upload_to_arduino(user_path, user_ports[i])
        
    upload_to_arduino(router_path, router_port)

    print("Arduino sketches were uploaded")

    process1.start()
    # process2.start()
    # process3.start()
    process_router.start()

    print("Processes are started")
    
    process1.join()
    # process2.join()
    # process3.join()
    process_router.join()