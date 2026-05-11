# type: ignore
import numpy as np
import pyvista as pv


def sf_to_cart(fi, theta, r):
    x = r * np.sin(theta) * np.cos(fi)
    y = r * np.sin(theta) * np.sin(fi)
    z = r * np.cos(theta)
    return x, y, z


# Tvoj originalni mgrid
fi, theta = np.mgrid[0 : 2 * np.pi : 120j, 0 : 2 * np.pi : 120j]
r = np.sin(theta) ** 2 * np.cos(theta) ** 2

x, y, z = sf_to_cart(fi, theta, r)

# --- PYVISTA DIO ---

# 1. Kreiramo strukturu mreže (StructuredGrid) iz x, y, z matrica
grid = pv.StructuredGrid(x, y, z)

# 2. Postavljamo "plotter" (ekvivalent mlab scene-u)
plotter = pv.Plotter(
    off_screen=False
)  # off_screen=True ako samo spremaš sliku bez prozora

# 3. Dodajemo plohu (ekvivalent mlab.mesh)
# PyVista nema 'Set3' identičnu Mayaviju, ali 'Set3' ili 'viridis' rade super
plotter.add_mesh(grid, cmap="Set3", smooth_shading=True)

# Ako želiš onu verziju s "mesh" (žičana mreža), otkomentiraj ovo:
# plotter.add_mesh(grid, style='wireframe', color='black', line_width=1)

# 4. Pozadina (mlab.gcf().scene.background = (1, 0, 0))
plotter.set_background("red")
plotter.show_axes()

# 5. Spremanje slike (mlab.savefig)
# plotter.screenshot("./plohaSferne1.png")

# 6. Prikaz (mlab.show)
plotter.show()
