from beamformer_api import BeamformerAPI
import time


def main():
    # Initialize the Beamformer API
    beamformer = BeamformerAPI(serial_port='COM3', baud_rate=115200)
    # beamformer_tcp = BeamformerAPI(tcp_host='192.168.50.10', tcp_port=2000)

    # Connect to the Beamformer
    beamformer.connect()

    # Initialization
    beamformer.beamformer_set_num_boards(2)  # Set the hardware(how many stacks are connected)
    beamformer.beamformer_init()

    # Set the firmware: number of elements per beams and, de facto, number of beams. In this case: 3 beams.
    beams_enumeration = [4, 4, 8]
    beamformer.beamformer_set_beams_enumeration(beams_enumeration)
    beamformer.beamformer_beams_init()
    time.sleep(1)

    # Communicate with the beamformer
    # Commands from the beamformer can be sent directly with the method 'beamformer_write()'
    beamformer.beamformer_write("help", sleep_time=0.25)
    beamformer.beamformer_write("info", sleep_time=0.25)

    # Testing the LEDs
    print("TESTING: LEDs")
    # Blink the LEDs sequentially of board 0 (top stack)
    beamformer.LED_demo_board(0)

    # Get the actual configuration of the beamformer (bits on each channel)
    print(beamformer.beamformer_write("get_beamformer", sleep_time=0.25))

    # Close the connection when done
    beamformer.disconnect()


if __name__ == "__main__":
    main()
