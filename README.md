# Beamformer API

This repository contains a Python script for controlling a custom beamformer device via serial or TCP connections. The script is composed of two files: `beamformer_api.py` (the API) and a controller that utilizes this API.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Methods](#api-methods)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use the Beamformer API, ensure you have Python installed on your system. You will also need the `pyserial` library. You can install it using pip:

```bash
pip install pyserial
```

## Usage
To use the Beamformer API, you need to create an instance of the BeamformerAPI class and connect to your device. The Controller.py file demonstrates how to use the API for both serial and TCP connections.

### Example Usage

```python
from beamformer_api import BeamformerAPI
import time

def main():
    # Example usage for serial connection
    beamformer_serial = BeamformerAPI(serial_port='COM10')
    beamformer_serial.connect()

    # Example usage for TCP connection
    beamformer_tcp = BeamformerAPI(tcp_host='192.168.50.10', tcp_port=2000)
    beamformer_tcp.connect()

    # Initialize the Beamformer API
    beamformer = BeamformerAPI(serial_port='COM3', baud_rate=115200)
    beamformer.connect()

    # Initialization
    beamformer.beamformer_set_num_boards(1)
    beamformer.beamformer_init()

    beams_enumeration = [[1]](https://sebhastian.com/modulenotfounderror-no-module-named-serial/)
    beamformer.beamformer_set_beams_enumeration(beams_enumeration)
    beamformer.beamformer_beams_init()
    time.sleep(1)

    # TESTING
    print("TESTING: LEDs ON 1s")
    beamformer.beamformer_write("LED_on", sleep_time=0.1)
    time.sleep(1)
    beamformer.beamformer_write("LED_off", sleep_time=0.1)
    time.sleep(1)

    beam_id = 0
    distance = 0.102
    num_x = 2
    num_y = 4
    frequency = 1575
    elevation = 20
    azimuth = 220

    print("Set 2D Beam")
    beamformer.set_2d_beam(beam_id, distance, num_x, num_y, frequency, elevation, azimuth)

    # Get the actual configuration of the beamformer (bits on each channel)
    print(beamformer.beamformer_write("get_beamformer", sleep_time=0.25))

    # Close the connection when done
    beamformer.disconnect()

if __name__ == "__main__":
    main()
```

## API Methods

__BeamformerAPI__

____init__(self, serial_port=None, baud_rate=115200, timeout=2, read_timeout=1, tcp_host=None, tcp_port=None)__

Initializes the BeamformerAPI instance.

Parameters:

    serial_port: The serial port to connect to (e.g., 'COM3').
    baud_rate: The baud rate for the connection (default is 115200).
    timeout: Timeout for the connection (default is 2 seconds).
    read_timeout: Timeout for reading data (default is 1 second).
    tcp_host: Host for TCP connection (if applicable, example: 192.168.50.50).
    tcp_port: Port for TCP connection (if applicable, example: 2000).

__connect()__

Establishes a connection to the beamformer device.

__disconnect()__

Disconnects from the beamformer device.

__check_connection()__

Checks if the connection to the beamformer is active.

__beamformer_init()__
Initialize the beamformer (to be performed after changing the number of boards).

__beamformer_beams_init()__
Initialize the beam configuration (to be performed after changing the beam configuration).

__beamformer_write(command, include_newline=True, sleep_time=0.050)__

Sends a command to the beamformer and returns the response.
Parameters:

    command: The command to send.
    include_newline: Whether to append a newline character to the command.
    sleep_time: Delay to wait for incoming data.

__beamformer_set_num_boards(num_boards_to_set)__
Command to set the hardware: set the connected number of boards in the beamformer.

__beamformer_get_num_boards()__
Get command: print the actual configured number of boards in the beamformer.

__beamformer_set_beams_enumeration(beams_enumeration)__
Command to set the hardware: set the beams configuration. Example: beamformer_set_beams_enumeration(4,4,8,8) will set 4 beams: 
    
    beam 0 : 4 elements, CH1-4 of first board
    beam 1 : 4 elements, CH5-8 of first board
    beam 2 : 8 elements, CH1-8 of second board
    beam 3 : 8 elements, CH1-8 of third board

__beamformer_get_beams_enumeration()__
Get command: print the actual configuration of beams.

__set_1d_beam(beamID, d_mm, freq_MHz, angle_deg)__
Configure a specified beam (*beamID*) to do linear beamforming at specified frequency (*freq_MHz*) and elevation angle in degree (*angle_deg*). The inter-element distance has to be set (with *d_mm*).

__set_2d_beam(beamID, d_mm, num_x, num_y, freq_MHz, elevation_angle, azimuth_angle)__
Configure a specified beam to do 2D (elevation/azimuth) beamforming.
Parameters to specify:

    beamID              beam identification number
    d_mm                inter-element spacing
    num_x               number of columns
    num_y               number of rows
    freq_MHz            frequency (MHz)
    elevation_angle     elevation angle in degree
    azimuth_angle       azimuth angle in degree

__set_element_phase(beamID, elementID, phase_shift)__
Configure a specified element to a choosen phase.
Parameters to specify:

    beamID              beam identification number
    elementID           element identification number
    phase_shift         phase shift to apply in degree


__LED_demo_board(boardID)__
Blink the LED on a specified board (index start at 0).

## Example usage
An example usage is provided in *Controller.py*

## License
This project is licensed under the MIT License - see the LICENSE file for details.