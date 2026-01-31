#importing packages/libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr

#opening the NetCDF file (note: this will be updated once I know how to create a configuration file
dset = xr.open_dataset(r'/Users/salhi/Downloads/Course_Data/SRTMGL1_NC.003_Data/N21E039.SRTMGL1_NC.nc')

#break for debugging
pdb.set_trace()

#storing elevation data in an array & closing the file
DEM = np.array(dset.variables['SRTMGL1_DEM'])
dset.close()

#break for debugging
pdb.set_trace()

#plotting DEM data
plt.imshow(DEM)

#adding a colorbar and its label
cbar = plt.colorbar()
cbar.set_label('Elevation (m asl)')

#saving the figure in a png file with 300dpi resolution
plt.savefig('assignment 1.png', dpi=300)
