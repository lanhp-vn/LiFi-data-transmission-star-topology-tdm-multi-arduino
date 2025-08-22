# Data Communications Final Project

A comprehensive implementation of serial communication protocols using Arduino microcontrollers, demonstrating single transceiver communication and Time Division Multiplexing (TDM) with clock synchronization.

## Project Overview

This project implements and tests various data communication protocols using Arduino Uno boards connected via serial communication. The implementation includes:

1. **Single Transceiver Communication** - Basic point-to-point communication through a router
2. **Clock-Synchronized TDM** - Multiple users sharing communication channels using time slots
3. **Advanced TDM with Addressing** - Enhanced TDM with timeout and broadcast timestamp features

## Hardware Requirements

### Optical Transceiver Components

Each transceiver consists of three key components:

1. **TX (Transmit) Module:**
   - **Users:** 650nm laser module (red laser diode)
   - **Router:** 940nm LED diode (infrared)

2. **RX (Receive) Module:**
   - **Users:** Photodetector capable of receiving 650nm laser light
   - **Router:** Photodetector capable of receiving 940nm infrared (IR) light

3. **Arduino Uno Board:** Microcontroller responsible for processing the TX/RX modules

### Complete Hardware List

- **4x Arduino Uno microcontrollers** (1 router + 3 users)
- **3x 650nm laser modules** (for user transmitters)
- **1x 940nm LED diode** (for router transmitter)  
- **4x Photodetector modules** (compatible with respective wavelengths)
- **Optical alignment components** (for laser/LED to photodetector alignment)
- **USB cables** for programming and power
- **Computer** with multiple USB ports or USB hub
- **Breadboards and connecting wires** for circuit assembly

**Signal Flow:**
- **User → Router:** 650nm laser light carries data from users to router
- **Router → User:** 940nm IR light carries synchronization and control signals from router to users

## Software Requirements

### Original Setup (VS Code - Deprecated)
The original implementation used VS Code with the Arduino extension, which has been deprecated.

### Recommended Setup (PlatformIO)
For reproducing this project, we recommend using **PlatformIO** instead:

1. Install [Visual Studio Code](https://code.visualstudio.com/)
2. Install the [PlatformIO IDE extension](https://platformio.org/platformio-ide)
3. Install Python 3.7+ for the automation scripts
4. Install required Python packages:
   ```bash
   pip install pyserial configparser
   ```

### Alternative Setup (Arduino CLI)
You can also use Arduino CLI as demonstrated in the automation scripts:
```bash
# Install Arduino CLI
# Configure for Arduino Uno boards
arduino-cli core install arduino:avr
```

## Project Structure

```
├── experiments/
│   ├── test2_single_transceiver/    # Basic single transceiver implementation
│   │   ├── Arduino_programs/
│   │   │   ├── main_transmit/       # Transmitter Arduino code
│   │   │   ├── main_receive/        # Receiver Arduino code
│   │   │   ├── main_router/         # Router Arduino code
│   │   │   └── test_connection/     # Connection test utilities
│   │   ├── Input_Output_files/      # Test data files
│   │   ├── config.ini               # Configuration parameters
│   │   ├── RUN.py                   # Main automation script
│   │   ├── main_transmit.py         # Python transmitter script
│   │   └── main_receive.py          # Python receiver script
│   ├── test3_clock_sync_tdm/        # TDM implementation with clock sync
│   │   ├── Arduino_programs/
│   │   │   ├── main_user/           # User node Arduino code
│   │   │   ├── main_router/         # Router Arduino code
│   │   │   └── test_connection/     # Connection test utilities
│   │   ├── Input_Output_files/      # User data files and outputs
│   │   ├── config.ini               # TDM configuration
│   │   ├── RUN.py                   # TDM automation script
│   │   ├── main_router.py           # Router Python script
│   │   ├── user1.py                 # User 1 Python script
│   │   ├── user2.py                 # User 2 Python script
│   │   └── user3.py                 # User 3 Python script
│   └── debug_needed/
│       ├── tdm_address_timeout/     # Advanced TDM with addressing/timeout (WIP)
│       └── broadcast_timestamp_tdm_address_timeout/  # WIP variant with timestamp broadcast
├── docs/
│   └── ProjectReport.pdf            # Project report
├── media/
│   ├── experimental_setup.png       # Hardware setup diagram
│   └── Test3_demo.mp4               # Local copy of demo (if needed)
└── README.md
```

## Implementation Details

### Test 2: Single Transceiver Communication

**Arduino Code Architecture:**

- **main_transmit.ino** (`main_transmit.ino:1-31`): Implements serial data transmission using SoftwareSerial at 700 baud. Reads data from PC via hardware serial and forwards to receiver via software serial.

- **main_receive.ino** (`main_receive.ino:1-23`): Receives data from transmitter using SoftwareSerial with inverted logic and forwards to PC via hardware serial.

- **main_router.ino** (`main_router.ino:1-32`): Acts as an intermediate router, receiving data from one Arduino and forwarding to another with packet framing using "++END++" delimiters.

**Key Features:**
- 700 baud serial communication
- Packet-based data transfer with end markers
- Configurable COM ports via `config.ini`
- Automated Arduino programming via Python scripts
- Bit Error Rate (BER) calculation

### Test 3: Clock-Synchronized TDM

Demo video: [YouTube – Test 3: Clock-Synchronized TDM](https://www.youtube.com/watch?v=9ShWfduWMxs)

**Arduino Code Architecture:**

- **main_router.ino** (`main_router.ino:1-78`): Implements TDM router with 5.1-second time slots. Collects data from users during listening periods and transmits timestamps for synchronization.

- **main_user.ino** (`main_user.ino:1-65`): User node implementation that synchronizes with router timestamp broadcasts and transmits data during assigned time slots.

**Key Features:**
- 1200 baud communication
- Configurable time slot duration and guard bands  
- Clock synchronization using timestamp broadcasts
- Multiple end signals for different packet types (`+++`, `~~~`, `---`)
- Support for 3 simultaneous users

### Configuration System

Both implementations use `config.ini` files for easy parameter adjustment:

**Single Transceiver Config:**
```ini
[param]
baud_rate = 1200
router_port = COM16
transmit_port = COM14
receive_port = COM7
```

**TDM Config:**
```ini
[param]
no_active_users = 3
baud_rate = 1200
timeslot_duration = 0.7
guard_band = 1
router_port = COM16
user1_port = COM14
user2_port = COM7
user3_port = COM6
```

## Usage Instructions

### For Test 2 (Single Transceiver):

1. **Hardware Setup:**
   - Connect 3 Arduino boards as per the experimental setup
   - Note the COM ports assigned to each Arduino

2. **Configuration:**
   - Edit `experiments/test2_single_transceiver/config.ini`
   - Update COM ports to match your system
   - Adjust baud rates if needed

3. **PlatformIO Setup:**
   ```bash
   # Create new PlatformIO project
   pio project init --board uno
   # Copy Arduino code to src/ folder
   # Upload to each Arduino individually
   pio run --upload-port COM14  # for transmitter
   pio run --upload-port COM7   # for receiver  
   pio run --upload-port COM16  # for router
   ```

4. **Run the Test:**
   ```bash
   cd experiments/test2_single_transceiver
   python RUN.py
   ```

### For Test 3 (TDM):

1. **Hardware Setup:**
   - Connect 4 Arduino boards (1 router + 3 users)
   - Record COM port assignments

2. **Configuration:**
   - Edit `experiments/test3_clock_sync_tdm/config.ini`
   - Update all user and router port assignments
   - Adjust timing parameters as needed

3. **Upload Code:**
   ```bash
   # Upload user code to 3 Arduino boards
   pio run --upload-port COM14  # user1
   pio run --upload-port COM7   # user2
   pio run --upload-port COM6   # user3
   # Upload router code  
   pio run --upload-port COM16  # router
   ```

4. **Run the TDM Test:**
   ```bash
   cd experiments/test3_clock_sync_tdm
   python RUN.py
   ```

## Code Functionality

### Automation Scripts (`RUN.py`)

The Python automation scripts handle:
- Dynamic Arduino code modification (baud rates, timing parameters)
- Automated code compilation and upload to multiple Arduinos
- Parallel execution of communication processes
- Data collection and BER analysis
- Synchronization of multiple serial connections

### Serial Communication Protocol

**Single Transceiver:**
- Uses packet framing with "++END++" terminators
- Implements store-and-forward routing
- Basic error detection through BER calculation

**TDM Implementation:**
- Time-slotted access with configurable durations
- Clock synchronization via timestamp broadcasts
- Guard bands prevent inter-slot interference
- Multiple signaling types for different message phases

## Troubleshooting

### Common Issues:

1. **COM Port Access:**
   - Ensure Arduino boards are properly connected
   - Check Device Manager (Windows) for port assignments
   - Close Arduino IDE/Serial Monitor before running scripts

2. **Upload Failures:**
   - Verify correct board selection in PlatformIO
   - Check USB cable connections
   - Ensure no other applications are using the COM ports

3. **Communication Errors:**
   - Verify baud rate consistency across all devices
   - Check wiring between Arduino boards
   - Monitor serial connections for proper data flow

4. **Python Dependencies:**
   ```bash
   pip install pyserial configparser multiprocessing subprocess
   ```

## Results and Analysis

The project demonstrates successful implementation of:
- Point-to-point serial communication with routing
- Multi-user time-division multiplexing
- Clock synchronization protocols
- Automated testing and BER analysis

Key performance metrics are calculated automatically, including bit error rates and timing analysis for the TDM implementation.

## Notes on Original Setup

**Important:** The original implementation used VS Code with the Arduino extension, which has been deprecated by Microsoft. The automation scripts (`RUN.py`) use `arduino-cli` commands that may need to be adapted for PlatformIO:

Replace arduino-cli commands with PlatformIO equivalents:
```python
# Original (arduino-cli)
cmd = f'arduino-cli compile --upload --port {port} --fqbn arduino:avr:uno {file_path}'

# PlatformIO equivalent  
cmd = f'pio run --upload-port {port} --project-dir {project_path}'
```

## Future Replication

- Migrate automation scripts to PlatformIO
- Implement error correction codes
- Add real-time performance monitoring
- Enhance TDM addressing and timeout mechanisms
- Add support for different Arduino board types