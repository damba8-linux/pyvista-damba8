# type: ignore
import os

import numpy as np
import pyvista as pv

# --- GEOMETRIJA (Boy Surface) ---
u_val, v_val = np.mgrid[0:1:100j, 0:1:100j]

u = u_val * np.pi
v = v_val * np.pi

# Sferne koordinate
X = np.cos(u) * np.sin(v)
Y = np.sin(u) * np.sin(v)
Z = np.cos(v)

b_const = np.sqrt(3) / 2

# F1, F2, F3 funkcije
f1 = 0.5 * (
    (2 * X**2 - Y**2 - Z**2) * (X**2 + Y**2 + Z**2)
    + 2 * Y * Z * (Y**2 - Z**2)
    + Z * X * (X**2 - Z**2)
    + X * Y * (Y**2 - X**2)
)

f2 = b_const * (
    (Y**2 - Z**2) * (X**2 + Y**2 + Z**2) + Z * X * (Z**2 - X**2) + X * Y * (Y**2 - X**2)
)

f3 = 0.125 * (X + Y + Z) * ((X + Y + Z) ** 3 + 4 * (Y - X) * (Z - Y) * (X - Z))

# Skaliranje i pozicioniranje
scale = 4.0
x = f1 * scale
y = f2 * scale
z = f3 * scale + 2.0

grid_surface = pv.StructuredGrid(x, y, z)

# --- 2. PLOTTER ---
plotter = pv.Plotter(lighting="light_kit")
plotter.set_background(color="#0a1a2a", top="#000000")
# for light in plotter.renderer.lights:
#    light.intensity = 0.8  # Priguši ih da dobiješ sjene

# --- HDR ---
hdr_path = "abandoned_tank_farm_04_1k.hdr"
if os.path.exists(hdr_path):
    tex = pv.read_texture(hdr_path)
    tex.interpolate = True
    tex.mipmap = True
    plotter.set_environment_texture(tex)
    try:
        plotter.renderer.SetEnvironmentEmphasis(2.2)
    except Exception:
        pass

# --- ZLATNA PLOHA + MREŽA ---
plotter.add_mesh(
    grid_surface,
    color="#FFD700",
    pbr=True,
    metallic=0.9,
    roughness=0.2,
    smooth_shading=True,
)

mesh_actor = plotter.add_mesh(
    grid_surface, style="wireframe", color="#cccccc", line_width=1, opacity=0.08
)
mesh_actor.mapper.SetResolveCoincidentTopologyToPolygonOffset()
mesh_actor.mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-3.0, -3.0)

# --- RAVNINE ---
# planeSize = 10 -> zidovi su na +/- 5
plane_size = 10.0
wall_offset = 5.0

# POD (Horizontalna ravnina na Z=0)
floor_xy = pv.Plane(
    center=(0, 0, 0), direction=(0, 0, 1), i_size=plane_size, j_size=plane_size
)

# ZADNJI ZID (y = 5, z = 5)
wall_back = pv.Plane(
    center=(0, wall_offset, wall_offset),
    direction=(0, 1, 0),
    i_size=plane_size,
    j_size=plane_size,
)

# LIJEVI ZID (x = -5, z = 5)
wall_left = pv.Plane(
    center=(-wall_offset, 0, wall_offset),
    direction=(1, 0, 0),
    i_size=plane_size,
    j_size=plane_size,
)

pbr_floor_args = dict(
    pbr=True, metallic=0.8, roughness=0.15, color="#4a69bd", opacity=0.8
)

plotter.add_mesh(floor_xy, **pbr_floor_args)
plotter.add_mesh(wall_back, **pbr_floor_args)
plotter.add_mesh(wall_left, **pbr_floor_args)

# Neon Grid Helperi na zidovima
grid_args = dict(style="wireframe", color="#00f2ff", opacity=0.2)
plotter.add_mesh(floor_xy, **grid_args)
plotter.add_mesh(wall_back, **grid_args)
plotter.add_mesh(wall_left, **grid_args)

# --- PROJEKCIJE (SJENE) ---
proj_args = dict(color="#001529", opacity=0.4, show_scalar_bar=False)

# Sjena na POD (Z=0)
proj_z = grid_surface.copy()
proj_z.points[:, 2] = 0.01
plotter.add_mesh(proj_z, **proj_args)

# Sjena na ZADNJI ZID
proj_y = grid_surface.copy()
proj_y.points[:, 1] = wall_offset - 0.01
plotter.add_mesh(proj_y, **proj_args)

# Sjena na LIJEVI ZID
proj_x = grid_surface.copy()
proj_x.points[:, 0] = -wall_offset + 0.01
plotter.add_mesh(proj_x, **proj_args)

# --- KAMERA ---
# PyVista koristi: position, focal_point, view_up
plotter.camera_position = [(14, -16, 10), (0, 0, 4), (0, 0, 1)]
plotter.camera.zoom(0.8)

print("Boyeva ploha VAU!")
plotter.show()
plotter.screenshot("./boy.jpeg")

# # Definiraj ime datoteke
# html_file = "boy_surface_vizualizacija.html"
# # Exportaj scenu
# # backend='vtkjs' je standardni i najstabilniji za interaktivni prikaz
# plotter.export_html(html_file)
# print(f"Gotovo! Otvori datoteku '{html_file}' u svom pregledniku.")
