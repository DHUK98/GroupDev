from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import csv


def initialise(dataset):
	# open dataset
	f = Dataset(dataset, "r", format="NETCDF4")

	# read in variables
	mt = f.variables['time']
	lat = f.variables['latitude']
	lon = f.variables['longitude']
	height = f.variables['height']
	pressure = f.variables['pressure']

	time = mt[:]
	lat = lat[:]
	lon = lon[:]
	height = height[:]
	pressure = pressure[:]

	f.close()	

	return time, lat, lon, height, pressure


def get_trajectory_array(dimension, n):
	# Return a 241 point array of the different data points for a particular dimension
	# dimension should be a string of either time, latitude, longitude, height, or pressure
	# n is which trajectory - from 0 to 8756. Each one is a different 241 point array for that particular aerosol particle's journey

	if n > 8756 or n < 0:
		print("Please use valid value for n")
		return
	else:
		switcher = {
			"time":time[n],
			"latitude":lat[n],
			"longitude":lon[n],
			"height":height[n],
			"pressure":pressure[n]
		}

		return switcher.get(dimension, "Invalid Dimension")


def plot_2D(X, Y, plot="scatter", xlabel="", ylabel=""):
	if plot == "line":
		plt.plot(X, Y)
	else:
		plt.scatter(X, Y)

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

	plt.show()
	return



if __name__ == "__main__":
	## EXAMPLE USAGE ###

	time, lat, lon, height, pressure = initialise("Trajectories/ERA-Interim_1degree_CapeGrim_100m_2016_hourly.nc")



	# number between 0 and 8756 to read, this is the trajectory you are going to choose
	n = 0

	# read in
	ntime = get_trajectory_array("time", n)
	nheight = get_trajectory_array("height", n)

	print(ntime)
	print(nheight)

	# # btw it appears most particles are measured for 10 days backwards from the time of sensing
	# print("Difference in time for this particle = ")
	# print(str(ntime[0]) + " - " + str(ntime[-1]) + " = " + str(ntime[0] - ntime[-1]) + " days")
	#
	# plot_2D(ntime, nheight, plot="line", xlabel="Time", ylabel="Height")



