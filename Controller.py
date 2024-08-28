from beamformer_api import BeamformerAPI
import time


def main():
    # Initialize the Beamformer API
    beamformer = BeamformerAPI(serial_port='COM3', baud_rate=115200)

    # Connect to the Beamformer
    beamformer.connect()

    # Initialization
    beamformer.beamformer_set_num_boards(1)
    beamformer.beamformer_init()

    beams_enumeration = [8]
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
    elevation = 10
    azimuth = 0

    print("Set 2D Beam")
    beamformer.set_2d_beam(beam_id,distance,num_x,num_y, frequency, elevation, azimuth)

    # Get the actual configuration of the beamformer (bits on each channel)
    print(beamformer.beamformer_write("get_beamformer", sleep_time=0.25))

    # Close the connection when done
    beamformer.disconnect()


if __name__ == "__main__":
    main()
