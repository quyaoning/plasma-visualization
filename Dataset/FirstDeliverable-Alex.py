import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

# Load data
df = pd.read_csv("makeup_data.csv")

particle_ids = sorted(df["particle_id"].unique())
n_particles = len(particle_ids)

# Sort each particle's trajectory into arrays
trajectories = {}
for pid in particle_ids:
    p = df[df["particle_id"] == pid].sort_values("time").reset_index(drop=True)
    trajectories[pid] = {
        "x": p["pos_x"].values,
        "y": p["pos_y"].values,
        "z": p["pos_z"].values,
        "t": p["time"].values,
    }

n_frames = len(next(iter(trajectories.values()))["t"])
times = next(iter(trajectories.values()))["t"]

# Color map by "is_ionized" values
type_colors = {0: "cyan", 1: "lime", 2: "orange"}

# Type 1 if is_ionized==1
ion_type = {}
colors = {}
for pid in particle_ids:
    vals = df[df["particle_id"] == pid]["is_ionized"]
    t = 1 if 1 in vals.values else vals.mode()[0]
    ion_type[pid] = t
    colors[pid] = type_colors[t]

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")
fig.patch.set_facecolor("#0d0d0d")
ax.set_facecolor("#0d0d0d")

# Axis limits
all_x = df["pos_x"].values
all_y = df["pos_y"].values
all_z = df["pos_z"].values
pad = 0.5
ax.set_xlim(all_x.min()-pad, all_x.max()+pad)
ax.set_ylim(all_y.min()-pad, all_y.max()+pad)
ax.set_zlim(all_z.min()-pad, all_z.max()+pad)

ax.set_xlabel("X", color="white")
ax.set_ylabel("Y", color="white")
ax.set_zlabel("Z", color="white")
ax.tick_params(colors="white")
ax.xaxis.pane.fill = ax.yaxis.pane.fill = ax.zaxis.pane.fill = False

title = ax.set_title("All Particles — t = 0.00", color="white", fontsize=12)

# Create a trail line and a dot for each particle
trails = {}
dots = {}
for pid in particle_ids:
    c = colors[pid]
    is_type1 = ion_type[pid] == 1

    lw = 2.0 if is_type1 else 0.6
    alpha = 0.9 if is_type1 else 0.4
    dotsize = 10 if is_type1 else 4
    edgewidth = 1.5 if is_type1 else 0

    trail, = ax.plot([], [], [], color=c, lw=lw, alpha=alpha)
    dot,   = ax.plot([], [], [], "*" if is_type1 else "o",
                     color=c, markersize=dotsize,
                     markerfacecolor=c, markeredgecolor="white",
                     markeredgewidth=edgewidth)
    trails[pid] = trail
    dots[pid] = dot


def init():
    for pid in particle_ids:
        trails[pid].set_data([], [])
        trails[pid].set_3d_properties([])
        dots[pid].set_data([], [])
        dots[pid].set_3d_properties([])
    return list(trails.values()) + list(dots.values())


def update(frame):
    for pid in particle_ids:
        x = trajectories[pid]["x"]
        y = trajectories[pid]["y"]
        z = trajectories[pid]["z"]
        trails[pid].set_data(x[:frame+1], y[:frame+1])
        trails[pid].set_3d_properties(z[:frame+1])
        dots[pid].set_data([x[frame]], [y[frame]])
        dots[pid].set_3d_properties([z[frame]])
    title.set_text(f"All Particles — t = {times[frame]:.2f}")
    return list(trails.values()) + list(dots.values())


# Benchmark: time 10 frames
print("Benchmarking update() across 10 frames...")
start = time.time()
for i in range(10):
    update(i)
elapsed = time.time() - start
avg_ms = elapsed / 10 * 1000
print(f"  Particles     : {n_particles}")
print(f"  Avg per frame : {avg_ms:.2f} ms")
print(f"  Estimated FPS : {1000/avg_ms:.1f}")
print(
    f"  Est. total    : {avg_ms * n_frames / 1000:.1f} s for {n_frames} frames")
print("-" * 40)

ani = animation.FuncAnimation(
    fig, update,
    frames=n_frames,
    init_func=init,
    interval=50,
    blit=False
)

plt.tight_layout()
plt.show()
