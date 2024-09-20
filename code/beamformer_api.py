import serial
import time
import numpy as np


def phase_shift_compute(num_col, num_row, d, f, theta, phi):
    c = 3e8  # Speed of light in m/s
    phase_shifts = np.zeros((num_row * num_col))  # Initialize an array
    theta_rad = np.deg2rad(theta)
    phi_rad = np.deg2rad(phi)

    element_index = 0
    # Compute the phase shift for the parameters
    for i in range(num_row):
        for j in range(num_col):
            phase_shifts[element_index] = 2 * np.pi * d * f / c * (
                    np.sin(theta_rad) * np.cos(phi_rad) * i + np.sin(theta_rad) * np.sin(phi_rad) * j)
            element_index = element_index + 1

    # Convert phase shifts to degrees
    phase_shifts = np.rad2deg(phase_shifts)
    return phase_shifts


class BeamformerAPI:
    def __init__(self, serial_port=None, baud_rate=115200, timeout=2, read_timeout=1, tcp_host=None, tcp_port=None):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.read_timeout = read_timeout
        self.tcp_host = tcp_host
        self.tcp_port = tcp_port
        self.beamformer = None

    def connect(self):
        try:
            if self.serial_port:
                print("Connecting to Beamformer via serial port...")
                self.beamformer = serial.Serial(self.serial_port, self.baud_rate, timeout=self.timeout)
            elif self.tcp_host and self.tcp_port:
                print("Connecting to Beamformer via TCP...")
                self.beamformer = serial.serial_for_url(f"socket://{self.tcp_host}:{self.tcp_port}",
                                                        baudrate=self.baud_rate, timeout=self.timeout)
            else:
                raise ValueError("Either serial_port or tcp_host and tcp_port must be provided.")

            time.sleep(2.5)
            print("Beamformer connected!")
        except (serial.SerialException, ValueError) as e:
            print(f"Error connecting to Beamformer: {e}")
            self.beamformer = None

    def disconnect(self):
        if self.beamformer:
            print("Disconnecting from Beamformer...")
            self.beamformer.close()
            self.beamformer = None
            print("Beamformer disconnected!")
        else:
            print("No active connection to disconnect.")

    def check_connection(self):
        if not self.beamformer or not self.beamformer.is_open:
            print("Beamformer not connected.")
            return False
        return True

    def beamformer_write(self, command, include_newline=True, sleep_time=0.050):
        if not self.beamformer:
            print("Error: Beamformer not connected.")
            return "Error"

        if isinstance(command, str):
            command = command.encode()

        if include_newline:
            command += b'\n'

        try:
            self.beamformer.write(command)
            time.sleep(sleep_time)
            response = self.beamformer.read_all().decode()
        except serial.SerialTimeoutException:
            print("Serial timeout error during communication.")
            return "Error"
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            return "Error"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Error"

        if "OK" in response.split('\r\n'):
            return response.strip()
        else:
            return "Error"

    def LED_demo_board(self, board_index):
        if not self.check_connection():
            return "Error, not connected"
        cmd_temp = f"LED_demo_board({board_index})"
        return self.beamformer_write(cmd_temp, sleep_time=1)

    def beamformer_get_num_boards(self):
        if not self.check_connection():
            return "Error, not connected"
        response = self.beamformer_write("get_num_boards")
        if response == "Error":
            return "Error"
        try:
            num_boards_bf = int(response.split('\r\n')[-1])
            return num_boards_bf
        except ValueError:
            return "Error"

    def beamformer_set_num_boards(self, num_boards_to_set):
        if not self.check_connection():
            return "Error, not connected"
        cmd_temp = f"set_num_boards({num_boards_to_set})"
        response = self.beamformer_write(cmd_temp)
        if "Invalid number of boards" in response:
            print("Invalid number of boards. Please enter a number between 1 and 8.")
            return "Error"
        return response

    def beamformer_set_update(self):
        if not self.check_connection():
            return "Error, not connected"
        response = self.beamformer_write("set_beamformer_update")
        if "Error" in response:
            print("Something went wrong, please check connection.")
            return "Error"
        return response

    def beamformer_init(self):
        if not self.check_connection():
            return "Error, not connected"
        response = self.beamformer_write("set_beamformer_init")
        if "Error" in response:
            print("Something went wrong, please check connection.")
            return "Error"
        return response

    def beamformer_get_beams_enumeration(self):
        if not self.check_connection():
            return "Error, not connected"
        response = self.beamformer_write("get_beamlist_param")
        if response == "Error":
            return "Error"
        try:
            response_parts = response.split('\r\n')[-1].split('(')
            beam_number = response_parts[0]
            beam_sizes = [int(size) for size in response_parts[1].rstrip(')').split(',')]
            return beam_number, beam_sizes
        except (IndexError, ValueError):
            return "Error"

    def beamformer_set_beams_enumeration(self, beams_enumeration):
        if not self.check_connection():
            return "Error, not connected"
        beams_enumeration_str = [str(size) for size in beams_enumeration]
        cmd_temp = f"configureBeamSizes({', '.join(beams_enumeration_str)})"
        return self.beamformer_write(cmd_temp)

    def beamformer_beams_init(self):
        if not self.check_connection():
            return "Error, not connected"
        response = self.beamformer_write("set_beamlist_init")
        if "Error" in response:
            print("Something went wrong, please check connection.")
            return "Error"
        return response

    def set_1d_beam(self, beam_index, d_mm, freq_MHz, angle_deg):
        if not self.check_connection():
            return "Error, not connected"
        cmd_temp = f"configureBeam({beam_index}, {d_mm}, {freq_MHz}, {angle_deg})"
        return self.beamformer_write(cmd_temp, sleep_time=0.1)

    # Do not use, for now there are some inversion error in the beamformer firmware, instead use 'set_beam_planar_array'
    def set_2d_beam(self, beam_index, d_mm, num_x, num_y, freq_MHz, elevation_angle, azimuth_angle):
        if not self.check_connection():
            return "Error, not connected"
        d_m = d_mm / 1000
        cmd_temp = f"set_2d_beam({beam_index}, {d_m}, {num_x}, {num_y}, {freq_MHz}, {elevation_angle}, {azimuth_angle})"
        return self.beamformer_write(cmd_temp, sleep_time=0.1)

    def set_element_phase(self, beam_index, element_index, phase_shift):
        if not self.check_connection():
            return "Error, not connected"
        cmd_temp = f"set_element_phase({beam_index}, {element_index}, {phase_shift})"
        return self.beamformer_write(cmd_temp, sleep_time=0.1)

    """
    @brief Configures the phase shift for a planar array of beamforming elements.
    @param beams_enumeration A list of integers, where each integer represents the number of elements in each beam for the beamformer.
    @param beam_index Index of the beam for which the phase shifts are to be configured.
    @param num_x Number of elements in the x-direction of the planar array.
    @param num_y Number of elements in the y-direction of the planar array.
    @param pitch Spacing between the elements of the planar array in meters (m).
    @param frequency Operating frequency of the beamformer in Hertz (Hz).
    @param theta Elevation angle in degrees. 0 degrees represents the zenith (directly overhead).
    @param phi Azimuth angle in degrees. 0 degrees typically points to where the array is initially directed (e.g., North).
    
    @return A string 'Done' when the configuration is completed successfully.
    """

    def set_beam_planar_array(self, beams_enumeration, beam_index, num_x, num_y, pitch, frequency, theta, phi):
        d = pitch
        f = frequency
        phase_shift_list = phase_shift_compute(num_x, num_y, d, f, theta, phi)
        for i in range(beams_enumeration[beam_index]):
            self.set_element_phase(beam_index, i, phase_shift_list[i])

        self.beamformer_set_update()
        return 'Done'
