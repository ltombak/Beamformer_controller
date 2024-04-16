import serial
import time

# Define the serial port and baud rate
serial_port = 'COM10'
baud_rate = 115200

# Initialize the serial connection
print("Connecting to Beamformer")
beamformer = serial.Serial(serial_port, baud_rate)
print("Beamformer connected !")
time.sleep(2)


def beamformer_write(command, include_newline=True, sleep_time=0.05):
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

    # Return the response
    if str(beamformer_response.split('\r\n')[1]) == "OK":
        return beamformer_response.strip()  # Strip leading/trailing whitespaces, '\r', and '\n'
    else:
        return "Error"


def beamformer_get_num_boards():
    get_num_boards = beamformer_write("get_num_boards")
    if get_num_boards == "Error":
        return "Error"
    else:
        num_boards_bf = int(get_num_boards.split('\r\n')[-1])  # Extract the last element after splitting by '\r\n'
        return num_boards_bf


def beamformer_set_num_boards(num_boards_to_set):
    cmd_temp = "num_boards(" + str(num_boards_to_set) + ")"
    cmd_sent = beamformer_write(cmd_temp)
    if cmd_sent.split('\r\n')[-1] == "Invalid number of boards. Please enter a number between 1 and 8.":
        print("Invalid number of boards. Please enter a number between 1 and 8.")
        return "Error"
    else:
        return


def beamformer_get_beams_enumeration():
    get_beams_enumeration = beamformer_write("get_beams_enumeration")
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
    print("---cmd_tmp:", cmd_temp)
    cmd_sent = beamformer_write(cmd_temp)
    if cmd_sent == "Error":
        return "Error"
    else:
        return


beams_enumeration = [2, 2, 2, 2, 4, 4, 8, 2]
beamformer_set_beams_enumeration(beams_enumeration)

beam_number, beam_sizes = beamformer_get_beams_enumeration()
print("Beam number:", beam_number)
print("Beam sizes:", beam_sizes)

# Configuration parameters
num_boards = beamformer_get_num_boards()
print("Number of boards:", num_boards)
beamformer_set_num_boards(4)

# print(beamformer_write("print_beam_list", sleep_time=0.1))
print(beamformer_write('info'))
# beamformer_write('LED_demo')

# beamformer.write(b'num_boards({})\n'.format(num_boards))
beamformer.close()
