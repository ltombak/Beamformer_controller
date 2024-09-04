from beamformer_api import BeamformerAPI
import time
import numpy as np

# Constants
c = 3e8  # Speed of light in m/s
f = 1575e6  # Frequency in Hz
d = 0.102  # Inter-element spacing in m

def phase_shift_compute(num_col, num_row, theta, phi):
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


def main():
    # Initialize the Beamformer API
    beamformer = BeamformerAPI(serial_port='COM3', baud_rate=115200)

    # Connect to the Beamformer
    beamformer.connect()

    # Initialization
    beamformer.beamformer_set_num_boards(2)
    beamformer.beamformer_init()

    beams_enumeration = [8,8]
    beamformer.beamformer_set_beams_enumeration(beams_enumeration)
    beamformer.beamformer_beams_init()
    time.sleep(1)

    beam_id = 0
    num_x = 2
    num_y = 4
    elevation = 20
    azimuth = 40

    phase_shift_list = phase_shift_compute(num_x, num_y, elevation, azimuth)
    print("Beam config: ")
    print(phase_shift_list)

    for i in range(beams_enumeration[beam_id]):
        beamformer.set_element_phase(beam_id, i, phase_shift_list[i])

    beamformer.beamformer_set_update()

    # Get the actual configuration of the beamformer (bits on each channel)
    print(beamformer.beamformer_write("get_beamformer", sleep_time=0.25))

    # Close the connection when done
    beamformer.disconnect()


if __name__ == "__main__":
    main()

