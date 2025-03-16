from geolib import geohash
from geopy.distance import geodesic
from shapely.geometry import Polygon

import numpy as np
import matplotlib.pyplot as plt

#Function to get Geohashes within Radius

def get_geohashes_within_radius(lat, lon, radius_km, precision):
    # Initialize an empty set to store geohashes
    geohashes = set()
    
    # Define the boundary box edges by moving in cardinal directions
    north_point = geodesic(kilometers=radius_km).destination((lat, lon), 0)
    south_point = geodesic(kilometers=radius_km).destination((lat, lon), 180)
    east_point = geodesic(kilometers=radius_km).destination((lat, lon), 90)
    west_point = geodesic(kilometers=radius_km).destination((lat, lon), 270)
    
    # Define the bounding box
    lat_min, lat_max = south_point.latitude, north_point.latitude
    lon_min, lon_max = west_point.longitude, east_point.longitude
    
    step_size = 0.001  # Define step size for the grid search
    for lat_step in np.arange(lat_min, lat_max, step_size):
        for lon_step in np.arange(lon_min, lon_max, step_size):
            ghhash = geohash.encode(lat_step, lon_step, precision)
            
            # Calculate the distance from the center point to the geohash point
            if geodesic((lat, lon), (lat_step, lon_step)).km <= radius_km:
                geohashes.add(ghhash)
                
    return sorted(geohashes)

# Example usage with synthetic data
lat, lon = 40.7128, -74.0060  # New York City coordinates
radius_km = 1.0  # 1 km radius
precision = 6  # Geohash precision level

geohashes = get_geohashes_within_radius(lat, lon, radius_km, precision)
print("Generated Geohashes:", geohashes)

#Visualize geohashes
def plot_geohashes(geohash_list, latitude, longitude, radius_km):
    
    fig, ax = plt.subplots(figsize=(5,5))
    
    #plot each geohashes as a polygon
    for ghash in geohash_list:
        #Decode the geohash bounds
        bounds = geohash.bounds(ghash)
        sw, ne = bounds[0], bounds[1]
        
        #Create polygons from bounds
        polygon = Polygon([
            (sw[1], sw[0]),
            (ne[1], sw[0]),
            (ne[1], ne[0]),
            (sw[1], ne[0]),
            (sw[1], sw[0])
        ])
        
        #plot polygon
        x, y = polygon.exterior.xy
        ax.fill(x, y, alpha=0.3, fc='blue', ec='blue')
    
    #convert radius from km to degrees for lat and lon
    # 1 degree latitude ~~ 111.139 km
    latitude=float(latitude)
    longitude=float(longitude)
    radius_lat_deg = radius_km / 111.139
    radius_lon_deg = radius_km / (111.139 * np.cos(np.radians(latitude)))
                                   
    #Draw a circle
    circle = plt.Circle((longitude,latitude), radius=radius_lon_deg, color='red', alpha=0.3, fill=False, linewidth=2)
    ax.add_patch(circle)
    
    #Center and zoom the map around the target area
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(f"Geohashes within {radius_km} km Radius around ({longitude}, {latitude})")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Example usage with synthetic data
lat, lon = 40.7128, -74.0060  # New York City coordinates
radius_km = 1.0  # 1 km radius
precision = 6  # Geohash precision level

neighbor_geohashes = get_geohashes_within_radius(lat, lon, radius_km, precision)

plot_geohashes(geohashes, lat, lon, radius_km)

