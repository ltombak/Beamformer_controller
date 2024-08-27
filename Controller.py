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

    beams_enumeration = [4, 4, 4, 4]
    beamformer.beamformer_set_beams_enumeration(beams_enumeration)
    beamformer.beamformer_beams_init()
    time.sleep(1)

    # TESTING
    print("TESTING: LEDs ON 5s")
    beamformer.beamformer_write("LED_on", sleep_time=0.1)
    time.sleep(5)
    beamformer.beamformer_write("LED_off", sleep_time=0.1)

    """
    beamformer.set_beam(0, 102, 1575, 0)
    beamformer.set_beam(1, 102, 1575, 10)
    beamformer.set_beam(2, 102, 1575, -10)
    """
    # Get the actual configuration of the beamformer (bits on each channel)
    print(beamformer.beamformer_write("get_beamformer", sleep_time=0.25))

    # Close the connection when done
    beamformer.disconnect()


if __name__ == "__main__":
    main()
