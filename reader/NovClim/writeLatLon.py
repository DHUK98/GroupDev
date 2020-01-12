from netCDF4 import Dataset
import csv


f = Dataset("Trajectories/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.nc", "r", format="NETCDF4")

lat = f.variables['latitude']
lon = f.variables['longitude']
lat = lat[:]
lon = lon[:]

headers = ['Lat', 'Lon']

with open("LatLonExample.csv", "w", newline='') as infile:
	csvwriter = csv.writer(infile, delimiter=",")
	csvwriter.writerow(headers)

	for i in range(len(lat)):
		csvwriter.writerow([lat[i][3], lon[i][3]])

