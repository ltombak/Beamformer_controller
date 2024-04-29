import numpy as np
import matplotlib.pyplot as plt

# Element numbers
N = 4
# Element spacing
d = 0.5
# Phase shift in degrees
phase_deg = 32

# Initialization of the parameters
An = 1
j = 1j  # Define the imaginary unit in Python

AF = np.zeros(360)
phase_rad = np.deg2rad(phase_deg)

for phi in range(360):
    # Change degree to radian
    phi_rad = np.deg2rad(phi)

    # Array factor calculation
    array_factor = 0
    for n in range(N):
        array_factor += An * np.exp(j * n * 2 * np.pi * d * (np.cos(phi_rad)) + j * n * phase_rad)

    AF[phi] = np.abs(array_factor)

# Plot the array factor
plt.polar(np.deg2rad(np.arange(360)), AF)

plt.show()
