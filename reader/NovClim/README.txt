README for NovClim NetCDF trajectory data
=========================================

The files contain trajectories initialised every hour for a given year.
The filenames should hopefully be self explanatory. There is no
guarantee that there will be the same number of trajectories in every
file. Additional variables will most likely be added in future.

The data is split by variable e.g. latitude, longitude etc. and each
variable represents all the trajectories in that file. Pay attention
to the dimensions described in the files as this will describe the
shape of the data.

To get started I strongly recommend using ncdump, see below. ncdump
piped into less e.g. `ncdump <file> | less` provides a quick and easy
way to inspect the data.


Tools for manipulating NetCDF data
----------------------------------
NetCDF-C libraries (for tools like ncdump):
    https://www.unidata.ucar.edu/software/netcdf/docs/getting_and_building_netcdf.html
netCDF4 in Python:
    https://unidata.github.io/netcdf4-python/netCDF4/index.html
NetCDF-Java:
    https://www.unidata.ucar.edu/software/netcdf-java/current/


Tools for inspecting NetCDF data
--------------------------------
xconv
    http://cms.ncas.ac.uk/documents/xconv/
ncview:
    http://meteora.ucsd.edu/~pierce/ncview_home_page.html
