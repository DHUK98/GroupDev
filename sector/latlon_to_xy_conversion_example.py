from pyproj import Proj, transform

# declare projections
inProj = Proj(init='epsg:4326')     # coordinate standard for GPS etc
outProj = Proj(init='epsg:3857')    # Projected coordinates used for rendering maps in GMaps etc


x1, y1 = -40, 144
x2, y2 = transform(inProj, outProj, x1, y1)

print(x2, y2)