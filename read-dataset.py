import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon


base_path = os.path.expanduser("~")
data_path = os.path.join(base_path, "data", "cimat", "incidents")

# Open CSV file, lat and lon are the coordinates
incidents_df = pd.read_csv(os.path.join(data_path, "incidents.csv"))
# Convert the datetime
incidents_df["open_date"] = pd.to_datetime(incidents_df["open_date"], format="%Y-%m-%d")

# Create a GeoDataFrame from DataFrame
geometry = [Point(xy) for xy in zip(incidents_df["lon"], incidents_df["lat"])]
incidents_gdf = gpd.GeoDataFrame(incidents_df, geometry=geometry)

# Create a bounding box with Golfo de México coordinates
bbox_coords = [
    (-97.5936111111111, 29.1838889),  # First point (longitude, latitude)
    (-97.5936111111111, 17.2583333),
    (-81.1236111111111, 17.2583333),
    (-81.1236111111111, 29.1838889),
]
bbox = Polygon(bbox_coords)

# Filter rows within bounding box
incidents_gm_gdf = incidents_gdf[incidents_gdf.within(bbox)]

# Define Sentinel-1, Sentinel-2 operating dates to filter incidents by date range
incidents_gm_sen1_gdf = incidents_gm_gdf.loc[
    (incidents_gm_gdf["open_date"] > "2014-04-03")
]
incidents_gm_sen2_gdf = incidents_gm_gdf.loc[
    (incidents_gm_gdf["open_date"] > "2015-06-23")
]

# Save filtered data
print(incidents_gm_gdf)
print(incidents_gm_sen1_gdf)
print(incidents_gm_sen2_gdf)


incidents_gm_gdf.to_csv(os.path.join(data_path, "gm_incidents.csv"), index=False)
incidents_gm_sen1_gdf.to_csv(
    os.path.join(data_path, "gm_sen1_incidents.csv"), index=False
)
incidents_gm_sen2_gdf.to_csv(
    os.path.join(data_path, "gm_sen2_incidents.csv"), index=False
)
