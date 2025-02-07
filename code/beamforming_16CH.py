import time

from beamformer_api import BeamformerAPI


def main():
    # Initialize the Beamformer API
    serial_port = 'COM3'
    baud_rate = 115200
    beamformer = BeamformerAPI(serial_port, baud_rate)

    # Connect to the Beamformer
    beamformer.connect()

    # Hardware Initialization
    num_stacks = 2
    beamformer.beamformer_set_num_boards(num_stacks)
    beamformer.beamformer_init()

    # Firmware Initialization
    beams_enumeration = [16]
    beamformer.beamformer_set_beams_enumeration(beams_enumeration)
    beamformer.beamformer_beams_init()
    time.sleep(1)

    # Beamforming parameters
    frequency = 1575e6
    pitch = 0.102
    num_x = 4
    num_y = 4

    # Beamforming
    theta = -20  # equivalent to the elevation but 0 is the zenith
    phi = 90  # equivalent to the azimuth, 0 is where the array is pointing (North is common rule)

    beamformer.set_beam_planar_array(beams_enumeration, 0, num_x, num_y, pitch, frequency, theta, phi)

    # Get the actual configuration of the beamformer (bits on each channel)
    print(beamformer.beamformer_write("get_beamformer", sleep_time=0.25))

    # Close the connection when done
    beamformer.disconnect()


if __name__ == "__main__":
    main()
