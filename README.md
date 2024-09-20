# Beamformer API

This repository contains multiple a Python scripts for controlling a custom beamformer device via serial or TCP connections. The script `beamformer_api.py` is the API to call methods from, the script `Controller.py` shows a basic usage of the API and how to connect and send commands to the beamformer. The script `beamforming_example.py` shows how to connect and use the beamforming capabilities of the beamformer.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Methods](#api-methods)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use the Beamformer API, ensure you have Python installed on your system. You will also need the `pyserial` and `numpy` library. You can install it using pip:

```bash
pip install pyserial
pip install numpy
```

## Usage
To use the Beamformer API, you need to create an instance of the BeamformerAPI class and connect to your device. The `Controller.py` file demonstrates how to use the API for both serial and TCP connections:

```python
from beamformer_api import BeamformerAPI
import time


def main():
    # Initialize the Beamformer API
    beamformer = BeamformerAPI(serial_port='COM3', baud_rate=115200)
    # beamformer_tcp = BeamformerAPI(tcp_host='192.168.50.10', tcp_port=2000)

    # Connect to the Beamformer
    beamformer.connect()

    # Initialization
    beamformer.beamformer_set_num_boards(2)  # Set the hardware(how many stacks are connected)
    beamformer.beamformer_init()

    # Set the firmware: number of elements per beams and, de facto, number of beams. In this case: 3 beams.
    beams_enumeration = [4, 4, 8]
    beamformer.beamformer_set_beams_enumeration(beams_enumeration)
    beamformer.beamformer_beams_init()
    time.sleep(1)

    # Communicate with the beamformer
    # Commands from the beamformer can be sent directly with the method 'beamformer_write()'
    beamformer.beamformer_write("help", sleep_time=0.25)
    beamformer.beamformer_write("info", sleep_time=0.25)

    # Testing the LEDs
    print("TESTING: LEDs")
    # Blink the LEDs sequentially of board 0 (top stack)
    beamformer.LED_demo_board(0)

    # Get the actual configuration of the beamformer (bits on each channel)
    print(beamformer.beamformer_write("get_beamformer", sleep_time=0.25))

    # Close the connection when done
    beamformer.disconnect()


if __name__ == "__main__":
    main()

```

## API Methods

__BeamformerAPI__

____init__(serial_port=None, baud_rate=115200, timeout=2, read_timeout=1, tcp_host=None, tcp_port=None)__

Initializes the BeamformerAPI instance.
Parameters:

    serial_port         The serial port to connect to (e.g., 'COM3').
    baud_rate           The baud rate for the connection (default is 115200).
    timeout             Timeout for the connection (default is 2 seconds).
    read_timeout        Timeout for reading data (default is 1 second).
    tcp_host            Host for TCP connection (if applicable, example: 192.168.50.10).
    tcp_port            Port for TCP connection (if applicable, example: 2000).

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

    command             The command to send.
    include_newline     Whether to append a newline character to the command.
    sleep_time          Delay to wait for incoming data.

__beamformer_set_num_boards(num_boards_to_set)__

Command to set the hardware: set the connected number of boards in the beamformer.

__beamformer_get_num_boards()__

Get command: print the actual configured number of boards in the beamformer.

__beamformer_set_beams_enumeration(beams_enumeration)__

Command to set the hardware: set the beams configuration. Example: beamformer_set_beams_enumeration(4,4,8,16) will set 4 beams: 
    
    beam 0 : 4 elements, CH1-4 of first board
    beam 1 : 4 elements, CH5-8 of first board
    beam 2 : 8 elements, CH1-8 of second board
    beam 3 : 16 elements, CH1-8 of third board and CH1-8 of fourth board

board 0 is in the top stack.

__beamformer_get_beams_enumeration()__

Get command: print the actual configuration of beams.

__set_1d_beam(beam_index, d_mm, freq_MHz, angle_deg)__

Configure a specified beam (*beam_index*) to do linear beamforming at specified frequency (*freq_MHz*) and elevation angle in degree (*angle_deg*). The inter-element distance has to be set (with *d_mm*).

__set_beam_planar_array(beams_enumeration, beam_index, num_x, num_y, pitch, frequency, theta, phi)__

Configure a specified beam to do 2D (elevation/azimuth) beamforming for a planar array.
Parameters to specify:

    beams_enumeration   beam_enumeration variable to be passed
    beam_index          beam identification number
    num_x               number of columns
    num_y               number of rows
    pitch               inter-element spacing
    frequency           frequency (Hz, can be written 1575e6 for example)
    theta               elevation angle in degree
    phi                 azimuth angle in degree

__set_element_phase(beam_index, element_index, phase_shift)__

Configure a specified element to a chosen phase.
Parameters to specify:

    beam_index          beam identification number
    element_index       element identification number
    phase_shift         phase shift to apply in degree


__LED_demo_board(board_index)__

Blink the LEDs on a specified board (index start at 0).

## License
This project is licensed under the GNU License - see the LICENSE file for details.