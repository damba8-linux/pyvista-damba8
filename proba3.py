# type: ignore
import numpy as np
import pyvista as pv

# Generiraj 1,000,000 točaka (nasumični oblak)
n = 1000000
points = np.random.rand(n, 3)
cloud = pv.PolyData(points)

# Dodaj boju na temelju Z koordinate
cloud["height"] = points[:, 2]

# Prikaži s 'eye-dome lighting' (izgleda puno bolje za oblake točaka)
plotter = pv.Plotter()
plotter.add_mesh(cloud, scalars="height", cmap="magma", point_size=2)
plotter.enable_eye_dome_lighting()
plotter.show()
