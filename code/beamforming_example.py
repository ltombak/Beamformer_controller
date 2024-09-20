from beamformer_api import BeamformerAPI
import time
import numpy as np


def main():
    # Initialize the Beamformer API
    beamformer = BeamformerAPI(serial_port='COM3', baud_rate=115200)

    # Connect to the Beamformer
    beamformer.connect()

    # Initialization
    beamformer.beamformer_set_num_boards(2)
    beamformer.beamformer_init()

    beams_enumeration = [16]
    beamformer.beamformer_set_beams_enumeration(beams_enumeration)
    beamformer.beamformer_beams_init()
    time.sleep(1)

    frequency = 1575e6
    theta = -20  # equivalent to the elevation but 0 is the zenith
    phi = 90  # equivalent to the azimuth, 0 is where the array is pointing (North is common rule)
    beamformer.set_beam_planar_array(beams_enumeration, 0, 4, 4, 0.102, frequency, theta, phi)

    # Get the actual configuration of the beamformer (bits on each channel)
    print(beamformer.beamformer_write("get_beamformer", sleep_time=0.25))

    # Close the connection when done
    beamformer.disconnect()


if __name__ == "__main__":
    main()
