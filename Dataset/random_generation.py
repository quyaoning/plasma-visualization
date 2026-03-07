import numpy as np
import pandas as pd

np.random.seed(42)

initial_argons = 30     
initial_electrons = 20 
time_steps = 150             
dt = 0.02                    

data = []
next_particle_id = 1

for _ in range(initial_electrons):
    pid_e = next_particle_id
    next_particle_id += 1
    pos_e = np.array([np.random.uniform(-5.0, 10.0), np.random.normal(0, 3.0), np.random.normal(0, 3.0)])
    vel_e = np.array([np.random.normal(-5.0, 5.0), np.random.normal(-5.0, 5.0), np.random.normal(-5.0, 5.0)])
    
    for step in range(time_steps):
        t = step * dt
        data.append({
            'particle_id': pid_e,
            'is_ionized': 2,
            'time': round(t, 3),
            'pos_x': round(pos_e[0], 4),
            'pos_y': round(pos_e[1], 4),
            'pos_z': round(pos_e[2], 4)
        })
        vel_e += np.array([-15.0, 2.0, -2.0]) * dt
        pos_e += vel_e * dt


for _ in range(initial_argons):
    pid_ar = next_particle_id
    next_particle_id += 1
    
    pos_ar = np.array([0.0, np.random.normal(0, 1.5), np.random.normal(0, 1.5)])
    vel_ar = np.array([np.random.uniform(1.0, 3.0), np.random.normal(0, 0.2), np.random.normal(0, 0.2)])
    
    is_ionized = False
    ionization_x_threshold = np.random.uniform(5.0, 15.0)
    spawned_electron = None

    for step in range(time_steps):
        t = step * dt

        if not is_ionized and pos_ar[0] > ionization_x_threshold:
            is_ionized = True

        ionized= 1 if is_ionized else 0
        data.append({
            'particle_id': pid_ar,
            'is_ionized': ionized,
            'time': round(t, 3),
            'pos_x': round(pos_ar[0], 4),
            'pos_y': round(pos_ar[1], 4),
            'pos_z': round(pos_ar[2], 4)
        })

        if is_ionized:
            vel_ar += np.array([2.0, 0.5, 0.5]) * dt 
        else:
            vel_ar += np.random.normal(0, 0.1, 3) 

        pos_ar += vel_ar * dt

df = pd.DataFrame(data)
df.sort_values(by=['time', 'particle_id'], inplace=True)
filename = 'makeup_data.csv'
df.to_csv(filename, index=False)