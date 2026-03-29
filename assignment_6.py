import xarray
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tools

# Load dataset
dset = xarray.open_dataset(r'/Users/salhi/Downloads/reanalysis-era5-single-levels-timeseries-sfcyzr2jb0l.nc')

# Extract variables
t2m = np.array(dset.variables['t2m'])
tp = np.array(dset.variables['tp'])
latitude = np.array(dset.variables['latitude'])
longitude = np.array(dset.variables['longitude'])
time_dt = np.array(dset.variables['valid_time'])

# Convert units
t2m = t2m - 273.15
tp = tp * 1000

# Handle extra dimensions
if t2m.ndim == 4:
    t2m = np.nanmean(t2m, axis=1)
    tp = np.nanmean(tp, axis=1)

# Create DataFrame
df_era5 = pd.DataFrame(index=time_dt)
df_era5['t2m'] = t2m
df_era5['tp'] = tp

# Calculate mean annual precipitation
annual_precip = df_era5['tp'].resample('YE').mean() * 24 * 365.25
mean_annual_precip = np.nanmean(annual_precip)
print('mean annual precipitation = ', mean_annual_precip)

# Plot temperature and precipitation
df_era5.plot()
plt.show()

# Calculate potential evaporation (PE)
tmin = df_era5['t2m'].resample('D').min().values
tmax = df_era5['t2m'].resample('D').max().values
tmean = df_era5['t2m'].resample('D').mean().values
lat = 21.25
doy = df_era5['t2m'].resample('D').mean().index.dayofyear

pe = tools.hargreaves_samani_1982(tmin, tmax, tmean, lat, doy)

# Plot potential evaporation
ts_index = df_era5['t2m'].resample('D').mean().index
plt.figure()
plt.plot(ts_index, pe, label='Potential Evaporation')
plt.xlabel('Time')
plt.ylabel('Potential evaporation (mm d−1)')
plt.show()

# Calculate mean annual PE
annual_pe = pd.Series(pe, index=ts_index).resample('YE').sum()
mean_annual_pe = np.nanmean(annual_pe)
print('mean annual PE = ', mean_annual_pe)
