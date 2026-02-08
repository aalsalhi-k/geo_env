import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load historical data (1850-1900)
dset = xr.open_dataset(r'/Users/salhi/Downloads/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc')
mean_1850_1900 = np.mean(dset['tas'].sel(time=slice('18500101','19001231')), axis=0)

# Convert longitude from 0-360 to -180-180
lon = dset['lon'].values
if lon.max() > 180:
    mean_1850_1900 = np.roll(mean_1850_1900, len(lon)//2, axis=1)
mean_1850_1900 = np.array(mean_1850_1900)

# Load SSP119 data (2071-2100)
dset = xr.open_dataset(r'/Users/salhi/Downloads/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp119_r1i1p1f1_gr1_201501-210012.nc')
mean_2015_2100_ssp119 = np.mean(dset['tas'].sel(time=slice('20710101','21001231')), axis=0)
lon = dset['lon'].values
if lon.max() > 180:
    mean_2015_2100_ssp119 = np.roll(mean_2015_2100_ssp119, len(lon)//2, axis=1)
mean_2015_2100_ssp119 = np.array(mean_2015_2100_ssp119)

# Load SSP245 data (2071-2100)
dset = xr.open_dataset(r'/Users/salhi/Downloads/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp245_r1i1p1f1_gr1_201501-210012.nc')
mean_2015_2100_ssp245 = np.mean(dset['tas'].sel(time=slice('20710101','21001231')), axis=0)
lon = dset['lon'].values
if lon.max() > 180:
    mean_2015_2100_ssp245 = np.roll(mean_2015_2100_ssp245, len(lon)//2, axis=1)
mean_2015_2100_ssp245 = np.array(mean_2015_2100_ssp245)

# Load SSP585 data (2071-2100)
dset = xr.open_dataset(r'/Users/salhi/Downloads/Course_Data/Climate_Model_Data/tas_Amon_GFDL-ESM4_ssp585_r1i1p1f1_gr1_201501-210012.nc')
mean_2015_2100_ssp585 = np.mean(dset['tas'].sel(time=slice('20710101','21001231')), axis=0)
lon = dset['lon'].values
if lon.max() > 180:
    mean_2015_2100_ssp585 = np.roll(mean_2015_2100_ssp585, len(lon)//2, axis=1)
mean_2015_2100_ssp585 = np.array(mean_2015_2100_ssp585)

# Calculate global min and max 
all_data = [mean_1850_1900, mean_2015_2100_ssp119, mean_2015_2100_ssp245, mean_2015_2100_ssp585]
vmin = min([data.min() for data in all_data])
vmax = max([data.max() for data in all_data])

# Function to plot and save 
def plot_temperature_map(data, title, filename, vmin, vmax):
    fig = plt.figure(figsize=(12, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Plot the data
    im = ax.imshow(data, origin='lower', extent=[-180, 180, -90, 90], 
                   transform=ccrs.PlateCarree(), cmap='jet', 
                   vmin=vmin, vmax=vmax)
    
    # Add country boundaries and coastlines
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor='black')
    
    # Add title
    ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Add colorbar with label
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar.set_label('Temperature (K)')
    
    # Save figure
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Plot all four scenarios 
plot_temperature_map(mean_1850_1900, 'Mean Temperature 1850-1900 (Historical)', 
                     'assignment2_historical_1850-1900.png', vmin, vmax)
plot_temperature_map(mean_2015_2100_ssp119, 'Mean Temperature 2071-2100 (SSP1-1.9)', 
                     'assignment2_ssp119_2071-2100.png', vmin, vmax)
plot_temperature_map(mean_2015_2100_ssp245, 'Mean Temperature 2071-2100 (SSP2-4.5)', 
                     'assignment2_ssp245_2071-2100.png', vmin, vmax)
plot_temperature_map(mean_2015_2100_ssp585, 'Mean Temperature 2071-2100 (SSP5-8.5)', 
                     'assignment2_ssp585_2071-2100.png', vmin, vmax)