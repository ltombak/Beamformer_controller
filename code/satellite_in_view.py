import ephem
import datetime


def read_tle_file(tle_file):
    with open(tle_file, 'r') as file:
        lines = file.readlines()
    satellites = []
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()
        satellites.append((name, line1, line2))
    return satellites


def compute_satellite_position(satellite, observer):
    sat = ephem.readtle(satellite[0], satellite[1], satellite[2])
    sat.compute(observer)
    return sat.alt, sat.az


def convert_to_decimal_degrees(angle):
    degrees, minutes, seconds = map(float, str(angle).split(':'))
    return degrees + (minutes / 60) + (seconds / 3600)


def get_visible_satellites(tle_file, observer_lat, observer_lon, observer_elev, observation_time, elevation_mask):
    observer = ephem.Observer()
    observer.lat = str(observer_lat)
    observer.lon = str(observer_lon)
    observer.elevation = observer_elev
    observer.date = observation_time

    satellites = read_tle_file(tle_file)
    visible_satellites = []

    for satellite in satellites:
        alt, az = compute_satellite_position(satellite, observer)
        alt_decimal = convert_to_decimal_degrees(alt)
        if alt_decimal > elevation_mask:  # Satellite is above the elevation mask
            az_decimal = convert_to_decimal_degrees(az)
            visible_satellites.append((satellite[0], alt_decimal, az_decimal))

    return visible_satellites


def query_satellite(tle_file, satellite_name, observer_lat, observer_lon, observer_elev, observation_time, elevation_mask):
    observer = ephem.Observer()
    observer.lat = str(observer_lat)
    observer.lon = str(observer_lon)
    observer.elevation = observer_elev
    observer.date = observation_time

    satellites = read_tle_file(tle_file)
    for satellite in satellites:
        if satellite[0] == satellite_name:
            alt, az = compute_satellite_position(satellite, observer)
            alt_decimal = convert_to_decimal_degrees(alt)
            if alt_decimal > elevation_mask:
                az_decimal = convert_to_decimal_degrees(az)
                return alt_decimal, az_decimal
            else:
                print(f"Satellite {satellite_name} is below the elevation mask of {elevation_mask} degrees.")
                return None, None

    print(f"Satellite {satellite_name} not found in TLE file.")
    return None, None


if __name__ == "__main__":
    tle_file = 'gnss.txt'
    observer_lat = 37.7749  # Example: San Francisco latitude
    observer_lon = -122.4194  # Example: San Francisco longitude
    observer_elev = 10  # Example: Elevation in meters
    observation_time = datetime.datetime.utcnow()  # Current UTC time
    elevation_mask = 15  # Example: Elevation mask in degrees

    visible_satellites = get_visible_satellites(tle_file, observer_lat, observer_lon, observer_elev, observation_time,
                                                elevation_mask)
    for sat in visible_satellites:
        print(f"Satellite: {sat[0]}, Elevation: {sat[1]:.2f} degrees, Azimuth: {sat[2]:.2f} degrees")

    sat_to_track = 'GSAT0221 (GALILEO 25)'
    ele, azi = query_satellite(tle_file, sat_to_track, observer_lat, observer_lon, observer_elev, observation_time, elevation_mask)
    print(f"Elevation: {ele:.2f} degrees, Azimuth: {azi:.2f} degrees")
