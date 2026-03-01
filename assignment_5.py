import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import glob

# List all files from 00 to 12 UTC
file_paths = [
    r'/Users/salhi/Downloads/GRIDSAT-B1.2009.11.25.00.v02r01.nc',
    r'/Users/salhi/Downloads/GRIDSAT-B1.2009.11.25.03.v02r01.nc',
    r'/Users/salhi/Downloads/GRIDSAT-B1.2009.11.25.06.v02r01.nc',
    r'/Users/salhi/Downloads/GRIDSAT-B1.2009.11.25.09.v02r01.nc',
    r'/Users/salhi/Downloads/GRIDSAT-B1.2009.11.25.12.v02r01.nc',
]

# Constants for the rainfall rate equation
A = 1.1183e11
b = 3.6382e-2
c = 1.2

cumulative_rainfall = None

# Looping through the files

for fp in file_paths:
    dset = xr.open_dataset(fp)
    IR = np.array(dset.variables['irwin_cdr']).squeeze()
    IR = np.flipud(IR)
    
    # Convert to Celsius
    T_celsius = IR - 273.15
    T_kelvin = IR  
        
    # Rainfall rate (mm/hr)
    R = A * np.exp(-b * (T_kelvin ** c))
    
    rainfall_3hr = R * 3  # mm over 3 hours because each file is 3 hour
    
    if cumulative_rainfall is None:
        cumulative_rainfall = rainfall_3hr
        IR_last = T_celsius  # save last BT for plotting
    else:
        cumulative_rainfall += rainfall_3hr
        IR_last = T_celsius

    dset.close()

jeddah_lat = 21.5
jeddah_lon = 39.2

# Plot final BT from last file (12 UTC)
plt.figure(1)
plt.imshow(IR_last, extent=[-180.035, 180.035, -70.035, 70.035], aspect ='auto', origin='upper', cmap='gray_r', vmin=-80, vmax=40)
cbar = plt.colorbar()
cbar.set_label('Brightness temperature (degrees Celsius) - 12 UTC')
plt.scatter(jeddah_lon, jeddah_lat, color='red', s=6, marker='o', label='Jeddah')
plt.legend()
plt.savefig('BT_jeddah.png', dpi=300, bbox_inches='tight')

# Plot cumulative rainfall
plt.figure(2)
plt.imshow(cumulative_rainfall, extent=[-180.035, 180.035, -70.035, 70.035],
           aspect='auto', origin='upper', cmap='Blues', vmin=0, vmax=50)
cbar = plt.colorbar()
cbar.set_label('Cumulative Rainfall 00-12 UTC (mm)')
plt.scatter(jeddah_lon, jeddah_lat, color='red', s=6, marker='o', label='Jeddah')
plt.legend()
plt.savefig('Rainfall_jeddah.png', dpi=300, bbox_inches='tight')

plt.show()