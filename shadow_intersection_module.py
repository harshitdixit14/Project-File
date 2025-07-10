import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from astropy.coordinates import EarthLocation, AltAz, get_sun
from astropy.time import Time
import astropy.units as u
import numpy as np

def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def do_segments_intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


user_input = {}
obstacleCount=int(input("Enter number of obstacle"))

# input for day, date, time for calculating sun's elevation angle

# we can use python module astropy to fetch current day date time

# but to calculate sun's elevation angle we need latitude and longitude
# but we have taken the coordinates as integer values

# we can convert integer values to angles

# let's take latitude as x coordinate

# then (x/360)*100 radians

# sin(α)=sin(ϕ)sin(δ)+cos(ϕ)cos(δ)cos(ω)

# ϕ latitude of the location

# δ solar declination angle

# ω hour angle

# need to calculate both sun's elevation angle and azimuth's angle

# calculating hour angle and sun's declination angle

now=Time.now()
sun=get_sun(now)

# now calculating sun's elevation angle



# for each object I need to calculate solar elevation angle because for every
# object the latitude will be different


for i in range(0,obstacleCount):
    x=float(input("Enter x coordinate"))
    y=float(input("Enter y coordinate"))
    height=float(input("Enter height of obstacle"))
    user_input[(x,y)]=height

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for (x, y), h in user_input.items():
    ax.bar3d(x, y, 0, 3, 3, h, shade=True, alpha=0.6, color='skyblue')  # bar3d(x, y, z, dx, dy, dz)
    ax.text(x + 0.5, y + 0.5, h + 0.1, f'{h}', ha='center', va='bottom', fontsize=10, color='black')

ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Height')
ax.set_xlim(0, 90)
ax.set_ylim(0, 90)
ax.set_zlim(0, 6)

# sun's elevation angle for each obstacle

# printing the sun's elevation angle for each obstacle# printing the sun's elevation angle for each obstacle


# print(elevation_angle)

# now for every corresponding elevation angle we will calculate shadow we can calculate shadow height

# the angle of shadow can be found with azimuth angle

# but we have to calculate azimuth angle  with respect to each and every obstacle
# theta is denoted as azimuth angle

elevation_angle = []
azimuth_angle = []
for (x,y) in user_input:
    obs_location=EarthLocation(lat=x*u.deg,lon=y*u.deg)
    altaz=sun.transform_to(AltAz(obstime=now,location=obs_location))
    elevation_angle.append(altaz.alt.deg)
    if(360-altaz.az.deg<180):
        azimuth_angle.append(360-altaz.az.deg)
    elif(360-altaz.az.deg>=180):
        azimuth_angle.append(altaz.az.deg)
shadow_points_and_height={}

# we are not able to map correctly the user input coord with shadowed last coord
# because dictionaries are ordered in python !!


i=0
for (a,b) in user_input:
    shadow_height=(user_input[(a,b)]/np.tan(elevation_angle[i]))
    x_shadow_coord=(a+shadow_height*np.sin(azimuth_angle[i]))
    y_shadow_coord=(b+shadow_height*np.cos(azimuth_angle[i]))
    shadow_points_and_height[x_shadow_coord,y_shadow_coord,a,b]=shadow_height
    i+=1

for (a, b, c, d) in shadow_points_and_height:
    print("obstacle location:", a, b)
    print("last shadow point:", c, d)
    plt.plot([a, c], [b, d], color='red')

# now we will take two location to find if we will ever come in path of shadow

x=int(input("enter starting x coord"))
y=int(input("enter starting y coord"))
a=int(input("enter ending x coord"))
b=int(input("enter ending y coord"))

plt.plot([x, a], [y, b], color='red')

# create step vector

start_vector=np.array([x,y])
step_vector=np.array([a,b])

# then check for every obstacle shadow vector if it intersects or not

for (p, q, u, v) in shadow_points_and_height:
    origin_vector=np.array([p,q])
    end_vector=np.array([u,v])
    print(do_segments_intersect(start_vector,step_vector,origin_vector,end_vector))


plt.show()




