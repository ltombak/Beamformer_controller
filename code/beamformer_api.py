import serial
import time


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

    def LED_demo_board(self, board_id):
        if not self.check_connection():
            return "Error, not connected"
        cmd_temp = f"LED_demo_board({board_id})"
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

    def set_1d_beam(self, beamID, d_mm, freq_MHz, angle_deg):
        if not self.check_connection():
            return "Error, not connected"
        cmd_temp = f"configureBeam({beamID}, {d_mm}, {freq_MHz}, {angle_deg})"
        return self.beamformer_write(cmd_temp, sleep_time=0.1)

    def set_2d_beam(self, beamID, d_mm, num_x, num_y, freq_MHz, elevation_angle, azimuth_angle):
        if not self.check_connection():
            return "Error, not connected"
        d_m = d_mm/1000
        cmd_temp = f"set_2d_beam({beamID}, {d_m}, {num_x}, {num_y}, {freq_MHz}, {elevation_angle}, {azimuth_angle})"
        return self.beamformer_write(cmd_temp, sleep_time=0.1)

    def set_element_phase(self, beamID, elementID, phase_shift):
        if not self.check_connection():
            return "Error, not connected"
        cmd_temp = f"set_element_phase({beamID}, {elementID}, {phase_shift})"
        return self.beamformer_write(cmd_temp, sleep_time=0.1)