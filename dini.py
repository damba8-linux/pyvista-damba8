# type: ignore
import numpy as np
import pyvista as pv

# --- 1. Geometrija ---
rho, zeta = 1, 1.3
u, v = np.mgrid[0:4:100j, 0 : 4 * np.pi : 100j]

denom = np.cosh((u - v * np.cos(zeta)) / (rho * np.sin(zeta)))
x = rho * np.sin(zeta) / denom * np.cos(v / rho)
y = rho * np.sin(zeta) / denom * np.sin(v / rho)
z = u - rho * np.sin(zeta) * np.tanh((u - v * np.cos(zeta)) / (rho * np.sin(zeta)))

grid_surface = pv.StructuredGrid(x, y, z)
grid_surface["Visina"] = z.ravel(
    order="F"
)  # Čita se stupac po stupac (okomito), "C" <- redak po redak

# --- 2. Postavke vizualizacije ---
# plotter = pv.Plotter()
plotter = pv.Plotter(lighting="light_kit")

# Glavna ploha
plotter.add_mesh(
    grid_surface,
    scalars="Visina",
    cmap="magma",
    smooth_shading=True,
    specular=0.8,
    show_scalar_bar=False,
    ambient=0.2,  # Lagano unutarnje osvjetljenje da nije pretamno
)

# --- 3. PARAMETARSKE CRTE (Mreža na samoj plohi) ---
# 'style="wireframe"' iscrtava svaku liniju parametarskog grida
actor = plotter.add_mesh(
    grid_surface,
    style="wireframe",
    color="white",
    line_width=1,
    opacity=0.4,  # Suptilne bijele crte
    label="Parametri",
    # render_lines_as_tubes=True,
    # lighting=False,
)

# Force-aj pomak linija prema kameri
actor.mapper.SetResolveCoincidentTopologyToPolygonOffset()
actor.mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-1.0, -1.0)

# --- 4. SVIJETLIJI PODNI GRID ---
floor_z = np.min(z) - 0.5
floor_grid = pv.Plane(
    center=(0, 0, floor_z), i_size=5, j_size=5, i_resolution=40, j_resolution=40
)

# Iscrtavamo podni grid s jačom bojom (cyan/bijela mješavina)
plotter.add_mesh(
    floor_grid,
    style="wireframe",
    color="#00f2ff",  # Neon Cyan
    line_width=1.5,
    opacity=0.6,  # Puno vidljivije
)

# Dodajemo "centar" grida kao jače linije (osi)
origin_axes = pv.Axes()
plotter.add_actor(origin_axes.actor)  # type: ignore[reportArgumentType]

# --- 5. Ambijent i kamera ---
# plotter.set_background("#020205")  # Skoro crna, ali s mrvicom dubine
plotter.set_background("#000000", top="#0a0a20")  # type: ignore[reportArgumentType]
# plotter.import_environment_map(None)
# plotter.enable_ssao(radius=0.5, bias=0.05)
plotter.enable_anti_aliasing()

# Postavljanje kamere za dramatičan pogled
plotter.camera_position = [(10, -10, 8), (0, 0, 2), (0, 0, 1)]
plotter.camera.zoom(1.8)

print("Uživaj u pogledu!")
plotter.show()
