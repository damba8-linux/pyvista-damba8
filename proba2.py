import numpy as np
import pyvista as pv

# Napravi NumPy podatke (brdo)
x = np.arange(-10, 10, 0.05)
y = np.arange(-10, 10, 0.05)
x, y = np.meshgrid(x, y)
z = 5 * np.sin(np.sqrt(x**2 + y**2))

# Pretvori to u PyVista grid
grid = pv.StructuredGrid(x, y, z)
grid.plot(show_grid=True, cmap="viridis")
