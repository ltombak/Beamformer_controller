import satellite_in_view
from beamformer_api import BeamformerAPI
import time


def track_satellite(tle_file, satellite_name, observer_lat, observer_lon, observer_elev, elevation_mask, time_interval,
                    beamformer, beam_id, distance, num_x, num_y, frequency, elevation, azimuth):
    observation_time = satellite_in_view.datetime.datetime.utcnow()
    ele, az = satellite_in_view.query_satellite(tle_file, satellite_name, observer_lat, observer_lon, observer_elev,
                                                observation_time, elevation_mask)
    if ele is not None:
        print(f"Satellite {satellite_name} is at {ele:.2f} degrees elevation and {az:.2f} degrees azimuth.")
        print("Tracking satellite in 1s.")
        time.sleep(1)
        while ele > elevation_mask:
            observation_time = satellite_in_view.datetime.datetime.utcnow()
            ele, az = satellite_in_view.query_satellite(tle_file, satellite_name, observer_lat, observer_lon,
                                                        observer_elev, observation_time, elevation_mask)
            print(f"Satellite {satellite_name} is at {ele:.2f} degrees elevation and {az:.2f} degrees azimuth.")
            beamformer.set_2d_beam(beam_id, distance, num_x, num_y, frequency, elevation, azimuth)
            time.sleep(time_interval)
        print(f"Satellite {satellite_name} is now below elevation mask.")
        return
    else:
        print(f"Satellite {satellite_name} not found or below elevation mask.")
        return


def main():
    # Set the parameters
    tle_file = 'gnss.txt'
    observer_lat = '37.7749'
    observer_lon = '-122.4194'
    observer_elev = 0
    elevation_mask = 10
    satellite_to_track = 'BEIDOU-3 M25'
    time_interval = 30

    # Initialize the Beamformer API
    beamformer = BeamformerAPI(serial_port='COM3', baud_rate=115200)

    # Connect to the Beamformer
    beamformer.connect()

    # Initialization
    beamformer.beamformer_set_num_boards(2)
    beamformer.beamformer_init()

    beams_enumeration = [64]
    beamformer.beamformer_set_beams_enumeration(beams_enumeration)
    beamformer.beamformer_beams_init()
    time.sleep(1)

    # Set the parameters for the beamformer
    beam_id = 0
    distance = 0.102
    num_x = 2
    num_y = 4
    frequency = 1575
    elevation = 20
    azimuth = 220

    # Track the satellite
    track_satellite(tle_file, satellite_to_track, observer_lat, observer_lon, observer_elev, elevation_mask,
                    time_interval, beamformer, beam_id, distance, num_x, num_y, frequency, elevation, azimuth)


if __name__ == '__main__':
    main()