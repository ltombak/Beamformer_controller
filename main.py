import serial
import time

# Define the serial port and baud rate
serial_port = 'COM10'
baud_rate = 115200

# Initialize the serial connection, COM port or also TCP IP
print("Connecting to Beamformer")
beamformer = serial.Serial(serial_port, baud_rate)
print("Beamformer connected !")
time.sleep(2.5)


def beamformer_write(command, include_newline=True, sleep_time=0.050):
    # Encode command to bytes if it's a string
    if isinstance(command, str):
        command = command.encode()

    # Add newline character if include_newline is True
    if include_newline:
        command += b'\n'

    # Send the command to the Arduino
    beamformer.write(command)

    # Wait for the specified time to ensure the Arduino has time to respond
    time.sleep(sleep_time)

    # Read the response from the Arduino
    beamformer_response = beamformer.read_all().decode()
    """
    print("---debug START")
    print(beamformer_response)
    print("---debug END")
    """
    # Return the response
    if str(beamformer_response.split('\r\n')[1]) == "OK":
        return beamformer_response.strip()  # Strip leading/trailing whitespaces, '\r', and '\n'
    else:
        return "Error"


def LED_demo_board(board_id):
    cmd_temp = "LED_demo_board(" + str(board_id) + ")"
    cmd_sent = beamformer_write(cmd_temp, sleep_time=1)
    if cmd_sent == "Error":
        return "Error"
    else:
        return


def beamformer_get_num_boards():
    get_num_boards = beamformer_write("get_num_boards")
    if get_num_boards == "Error":
        return "Error"
    else:
        num_boards_bf = int(get_num_boards.split('\r\n')[-1])  # Extract the last element after splitting by '\r\n'
        return num_boards_bf


def beamformer_set_num_boards(num_boards_to_set):
    cmd_temp = "set_num_boards(" + str(num_boards_to_set) + ")"
    cmd_sent = beamformer_write(cmd_temp)
    if cmd_sent.split('\r\n')[-1] == "Invalid number of boards. Please enter a number between 1 and 8.":
        print("Invalid number of boards. Please enter a number between 1 and 8.")
        return "Error"
    else:
        return


def beamformer_get_beams_enumeration():
    get_beams_enumeration = beamformer_write("get_beamlist_param")
    if get_beams_enumeration == "Error":
        return "Error"
    else:
        response_parts = get_beams_enumeration.split('\r\n')[-1].split('(')
        beam_number = response_parts[0]
        beam_sizes = [int(size) for size in response_parts[1].rstrip(')').split(',')]
        return beam_number, beam_sizes


def beamformer_set_beams_enumeration(beams_enumeration):
    # Convert each element in beams_enumeration to a string
    beams_enumeration_str = [str(size) for size in beams_enumeration]

    # Concatenate the elements with commas and format the command
    cmd_temp = "configureBeamSizes(" + ", ".join(beams_enumeration_str) + ")"
    cmd_sent = beamformer_write(cmd_temp)
    if cmd_sent == "Error":
        return "Error"
    else:
        return


def set_beam(beamID, d_mm, freq_MHz, angle_deg):
    cmd_temp = "configureBeam(" + str(beamID) + ", " + str(d_mm) + ", " + str(freq_MHz) + ", " + str(angle_deg) + ")"
    cmd_sent = beamformer_write(cmd_temp, sleep_time=0.1)
    if cmd_sent == "Error":
        return "Error"
    else:
        return


def set_2d_beam(beamID, d_m, num_x, num_y, freq_MHz, elevation_angle, azimuth_angle):
    cmd_temp = "configureBeam(" + str(beamID) + ", " + str(d_m) + ", " + str(num_x) + ", " + str(num_y) + ", " + str(
        freq_MHz) + ", " + str(elevation_angle) + ", " + str(azimuth_angle) + ", " + ")"
    cmd_sent = beamformer_write(cmd_temp, sleep_time=0.1)
    if cmd_sent == "Error":
        return "Error"
    else:
        return


beamformer_write("LED_on", sleep_time=0.1)
time.sleep(1)
beamformer_write("LED_off", sleep_time=0.1)

beamformer_set_num_boards(2)
beamformer_write("set_beamformer_init", sleep_time=0.1)
beams_enumeration = [4, 4, 4, 4]
beamformer_set_beams_enumeration(beams_enumeration)
time.sleep(1)
set_beam(0, 102, 1575, 0)
set_beam(1, 102, 1575, 10)
set_beam(2, 102, 1575, -10)

# Get the actual configuration of the beamformer (bits on each channel)
print(beamformer_write("get_beamformer", sleep_time=0.25))

# function list:
"""
print(beamformer_write("info"))
beamformer_write("LED_demo", sleep_time=5)
beamformer_write("LED_on", sleep_time=1)
beamformer_write("LED_off", sleep_time=0.25)
LED_demo_board(0)

# Get the actual configuration of the beamformer (bits on each channel)
print(beamformer_write("get_beamformer", sleep_time=0.25))

# Do an update of the beamformer, i.e. load the beamformer configuration in the ICs
print(beamformer_write("get_beamformer", sleep_time=0.1))

# Get the number of board configured in the firmware
num_boards = beamformer_get_num_boards()
print("Number of boards:", num_boards)

# Set the number of boards (hardware count (1-8))
beamformer_set_num_boards(4)

# Initialize the beamformer (once the number of boards have been set. To be run once only.)
beamformer_write("set_beamformer_init", sleep_time=0.1)

# Get the actual configuration of the beamlist (beam number and associated sizes.
beam_number, beam_sizes = beamformer_get_beams_enumeration()
print("Beam number:", beam_number)
print("Beam sizes:", beam_sizes)

# Configuration of the beam number and beam sizes. The beams will be automatically attributed to the beamformer channels
beams_enumeration = [4, 4, 8, 8, 8]
beamformer_set_beams_enumeration(beams_enumeration)

# Get the complete beamlist configuration (which element associated to which channel
print(beamformer_write("get_beamlist_config", sleep_time=0.5))

# Initialize the beamlist, to be done after setting the beam_enumeration (number of beams with associated sizes)
beamformer_write("set_beamlist_init", sleep_time=0.1)

"""
beamformer.close()
