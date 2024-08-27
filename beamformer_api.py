import serial
import time


class BeamformerAPI:
    def __init__(self, serial_port='COM10', baud_rate=115200, timeout=2):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.beamformer = None

    def connect(self):
        try:
            print("Connecting to Beamformer...")
            self.beamformer = serial.Serial(self.serial_port, self.baud_rate, timeout=self.timeout)
            time.sleep(2.5)
            print("Beamformer connected!")
        except serial.SerialException as e:
            print(f"Error connecting to {self.serial_port}: {e}")
            self.beamformer = None

    def disconnect(self):
        if self.beamformer:
            self.beamformer.close()
            print("Beamformer connection closed.")

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
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            return "Error"

        if "OK" in response.split('\r\n'):
            return response.strip()
        else:
            return "Error"

    def LED_demo_board(self, board_id):
        cmd_temp = f"LED_demo_board({board_id})"
        return self.beamformer_write(cmd_temp, sleep_time=1)

    def beamformer_get_num_boards(self):
        response = self.beamformer_write("get_num_boards")
        if response == "Error":
            return "Error"
        try:
            num_boards_bf = int(response.split('\r\n')[-1])
            return num_boards_bf
        except ValueError:
            return "Error"

    def beamformer_set_num_boards(self, num_boards_to_set):
        cmd_temp = f"set_num_boards({num_boards_to_set})"
        response = self.beamformer_write(cmd_temp)
        if "Invalid number of boards" in response:
            print("Invalid number of boards. Please enter a number between 1 and 8.")
            return "Error"
        return response

    def beamformer_init(self):
        response = self.beamformer_write("set_beamformer_init")
        if "Error" in response:
            print("Something went wrong, please check connection.")
            return "Error"
        return response

    def beamformer_get_beams_enumeration(self):
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
        beams_enumeration_str = [str(size) for size in beams_enumeration]
        cmd_temp = f"configureBeamSizes({', '.join(beams_enumeration_str)})"
        return self.beamformer_write(cmd_temp)


    def beamformer_beams_init(self):
        response = self.beamformer_write("set_beamlist_init")
        if "Error" in response:
            print("Something went wrong, please check connection.")
            return "Error"
        return response

    def set_beam(self, beamID, d_mm, freq_MHz, angle_deg):
        cmd_temp = f"configureBeam({beamID}, {d_mm}, {freq_MHz}, {angle_deg})"
        return self.beamformer_write(cmd_temp, sleep_time=0.1)

    def set_2d_beam(self, beamID, d_m, num_x, num_y, freq_MHz, elevation_angle, azimuth_angle):
        cmd_temp = f"configureBeam({beamID}, {d_m}, {num_x}, {num_y}, {freq_MHz}, {elevation_angle}, {azimuth_angle})"
        return self.beamformer_write(cmd_temp, sleep_time=0.1)

# The class `BeamformerAPI` is now ready to be imported and used in other scripts.
