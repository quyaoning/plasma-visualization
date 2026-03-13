import numpy as np
import pyvista as pv
import pandas as pd
import time

filename = "Dataset/makeup_data.csv"

df = pd.read_csv(filename)
df.sort_values("time", inplace=True)

plotter = pv.Plotter(window_size=(900,700))
plotter.set_background("white")

# -------------------------
# Fixed axes
# -------------------------
xmin, xmax = df['pos_x'].min(), df['pos_x'].max()
ymin, ymax = df['pos_y'].min(), df['pos_y'].max()
zmin, zmax = df['pos_z'].min(), df['pos_z'].max()

plotter.show_bounds(bounds=(xmin,xmax,ymin,ymax,zmin,zmax))

# -------------------------
# Initial frame
# -------------------------
first_time = df['time'].iloc[0]
frame = df[df["time"] == first_time]

points = frame[["pos_x","pos_y","pos_z"]].values
cloud = pv.PolyData(points)

plotter.add_mesh(
    cloud,
    render_points_as_spheres=True,
    point_size=8,
    color="red"
)

plotter.show(auto_close=False, interactive_update=True)

# -------------------------
# Animation loop
# -------------------------
for t, frame in df.groupby("time"):

    points = frame[["pos_x","pos_y","pos_z"]].values
    cloud.points = points

    plotter.update()
    time.sleep(0.01)

plotter.close()