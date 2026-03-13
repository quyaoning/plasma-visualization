import pyvista as pyv
import numpy as np
import pandas as pd
import time

data = pd.read_csv("./Dataset/makeup_data.csv")

plotter = pyv.Plotter(window_size=(900,700))
plotter.set_background("black")
#plotter.set_border_color("white")
plotter.add_box_axes()

# This part from Ujjwal's code
# -------------------------
# Fixed axes
# -------------------------
xmin, xmax = data['pos_x'].min(), data['pos_x'].max()
ymin, ymax = data['pos_y'].min(), data['pos_y'].max()
zmin, zmax = data['pos_z'].min(), data['pos_z'].max()

plotter.show_bounds(bounds=(xmin,xmax,ymin,ymax,zmin,zmax))

# End of Ujjwal's code

argon_color = 0
ionized_argon_color = 2
electron_color = 3.0

replacement_map = {'0': argon_color, '1': ionized_argon_color, '2': electron_color}


data['is_ionized'] = data['is_ionized'].replace(replacement_map)

data_dict = {name: group for name, group in data.groupby('time')}

point_cols = ['pos_x', 'pos_y', 'pos_z']
point_val_list = [data for data in data_dict.values()]


time_array = np.array(point_val_list)

point_mesh = pyv.PolyData(time_array[0][:, 3:])

point_mesh["colors"] = time_array[0][:, 1]

plotter.add_mesh(
    point_mesh, 
    scalars="colors", 
    point_size=10, 
    style="points",
    render_points_as_spheres=True
)

plotter.show(auto_close=False, interactive_update=True)

for arr in time_array :
    point_mesh.points = arr[:, 3:]
    point_mesh["colors"] = arr[:, 1]
    plotter.update()
    time.sleep(0.05)