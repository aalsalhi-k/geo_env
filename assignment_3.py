import tools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature

df_isd = tools.read_isd_csv(r'/Users/salhi/Downloads/41024099999.csv')

# Calculate RH and HI for hourly data
df_isd['RH'] = tools.dewpoint_to_rh(df_isd['DEW'].values, df_isd['TMP'].values)
df_isd['HI'] = tools.gen_heat_index(df_isd['TMP'].values, df_isd['RH'].values)

# resample HI directly using mean
df_daily['HI_from_hourly'] = df_isd['HI'].resample('D').mean()

plt.show
plot = df_isd.plot(title="ISD data for Jeddah")
plt.savefig("plot.png")

print(df_isd.max())
print(df_isd.idxmax())
print(df_isd.loc[["2024-08-10 11:00:00"]])

# Constants for the heat index calculation
c1 = -8.78469475556
c2 = 1.61139411
c3 = 2.33854883889
c4 = -0.14611605
c5 = -0.012308094
c6 = -0.0164248277778
c7 = 0.002211732
c8 = 0.00072546
c9 = -0.000003582
temp = 41
rh = 53.7797 
max_HI = c1 + c2*temp + c3*rh + c4*temp*rh + c5*temp*temp + c6*rh*rh + c7*temp*temp*rh + c8*temp*rh*rh + c9*temp*temp*rh*rh
print(max_HI)

# Create figure of HI time series for the year
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_daily.index, df_daily['HI_daily'], linewidth=2, label='Daily Heat Index')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Heat Index (°C)', fontsize=12)
ax.set_title('Daily Heat Index Time Series - Jeddah 2024', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig("daily_HI_timeseries.png", dpi=300, bbox_inches='tight')
plt.close()
