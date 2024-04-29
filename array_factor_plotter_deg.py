import numpy as np
import matplotlib.pyplot as plt

# Element numbers
N = 4
# Element spacing (lambda)
d = 0.5
# Phase shift in degrees
phase_deg = 0

# Initialization of the parameters
An = 1
j = 1j  # Define the imaginary unit in Python

# Define the range of angles to plot (from -90 degrees to 90 degrees)
angles_deg = np.arange(0, 181)

AF = np.zeros(len(angles_deg))
phase_rad = np.deg2rad(phase_deg)

for i, phi in enumerate(angles_deg):
    # Array factor calculation
    array_factor = 0
    for n in range(N):
        array_factor += An * np.exp(j * n * 2 * np.pi * d * (np.cos(np.deg2rad(phi)))) * np.exp(j * n * phase_rad)

    AF[i] = np.abs(array_factor)

# Plot the array factor in a Cartesian plot
custom_x = np.arange(-90, 91, 1)
plt.plot(custom_x, AF)

plt.xticks(np.arange(min(custom_x), max(custom_x)+1, 15))
plt.minorticks_on()
plt.grid()

plt.title('Array Factor vs. Angle')
plt.xlabel('Angle (degrees)')
plt.ylabel('Array Factor Magnitude')

plt.show()
