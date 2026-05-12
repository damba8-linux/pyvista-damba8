# type: ignore

import os

import numpy as np
import pyvista as pv

# =========================================================
# GEOMETRIJA (Boy Surface)
# =========================================================

u_val, v_val = np.mgrid[0:1:100j, 0:1:100j]

u = u_val * np.pi
v = v_val * np.pi

X = np.cos(u) * np.sin(v)
Y = np.sin(u) * np.sin(v)
Z = np.cos(v)

b_const = np.sqrt(3) / 2

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

scale = 4.0

x = f1 * scale
y = f2 * scale
z = f3 * scale + 2.0

grid_surface = pv.StructuredGrid(x, y, z)

# =========================================================
# PLOTTER
# =========================================================

plotter = pv.Plotter(
    lighting="light_kit",
    window_size=(1280, 720),
)

plotter.set_background(
    color="#0a1a2a",
    top="#000000",
)

for light in plotter.renderer.lights:
    light.intensity = 0.6

# =========================================================
# HDR
# =========================================================

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

try:
    plotter.renderer.GetEnvMapLookupTable()
    plotter.renderer.UseImageBasedLightingOn()
except Exception:
    pass

# =========================================================
# GLAVNA PLOHA
# =========================================================

gold_actor = plotter.add_mesh(
    grid_surface,
    color="#FFD700",
    pbr=True,
    metallic=1.0,
    roughness=0.2,
    smooth_shading=True,
)

mesh_actor = plotter.add_mesh(
    grid_surface,
    style="wireframe",
    color="#cccccc",
    line_width=1,
    opacity=0.08,
)

mesh_actor.mapper.SetResolveCoincidentTopologyToPolygonOffset()

mesh_actor.mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(
    -3.0,
    -3.0,
)

# =========================================================
# RAVNINE
# =========================================================

plane_size = 10.0
wall_offset = 5.0

floor_xy = pv.Plane(
    center=(0, 0, 0),
    direction=(0, 0, 1),
    i_size=plane_size,
    j_size=plane_size,
)

wall_back = pv.Plane(
    center=(0, wall_offset, wall_offset),
    direction=(0, 1, 0),
    i_size=plane_size,
    j_size=plane_size,
)

wall_left = pv.Plane(
    center=(-wall_offset, 0, wall_offset),
    direction=(1, 0, 0),
    i_size=plane_size,
    j_size=plane_size,
)

pbr_floor_args = dict(
    pbr=True,
    metallic=0.8,
    roughness=0.15,
    color="#4a69bd",
    opacity=0.8,
)

plotter.add_mesh(floor_xy, **pbr_floor_args)
plotter.add_mesh(wall_back, **pbr_floor_args)
plotter.add_mesh(wall_left, **pbr_floor_args)

grid_args = dict(
    style="wireframe",
    color="#00f2ff",
    opacity=0.2,
)

plotter.add_mesh(floor_xy, **grid_args)
plotter.add_mesh(wall_back, **grid_args)
plotter.add_mesh(wall_left, **grid_args)

# =========================================================
# PROJEKCIJE / SJENE
# =========================================================

proj_args = dict(
    color="#001529",
    opacity=0.4,
    show_scalar_bar=False,
)

proj_z = grid_surface.copy()
proj_z.points[:, 2] = 0.01

sh_floor_actor = plotter.add_mesh(
    proj_z,
    **proj_args,
)

proj_y = grid_surface.copy()
proj_y.points[:, 1] = wall_offset - 0.01

sh_back_actor = plotter.add_mesh(
    proj_y,
    **proj_args,
)

proj_x = grid_surface.copy()
proj_x.points[:, 0] = -wall_offset + 0.01

sh_left_actor = plotter.add_mesh(
    proj_x,
    **proj_args,
)

# =========================================================
# KAMERA
# =========================================================

plotter.camera_position = [
    (16, -18, 12),
    (0, 0, 4),
    (0, 0, 1),
]

plotter.camera.zoom(0.8)

# =========================================================
# HTML EXPORT
# =========================================================

plotter.export_html("boy_surface.html")

# =========================================================
# MP4 EXPORT
# =========================================================

plotter.open_movie(
    "boy_surface.mp4",
)

plotter.show(auto_close=False)

n_frames = 720  # glatko
angle_step = 360.0 / n_frames

for i in range(n_frames):
    # -------------------------------------
    # ROTACIJA PLOHE
    # -------------------------------------

    grid_surface.rotate_z(
        angle_step,
        inplace=True,
    )

    # -------------------------------------
    # UPDATE MESH-a
    # -------------------------------------

    gold_actor.mapper.dataset.points = grid_surface.points

    mesh_actor.mapper.dataset.points = grid_surface.points

    # -------------------------------------
    # UPDATE SJENA
    # -------------------------------------

    pts = grid_surface.points

    sh_floor_actor.mapper.dataset.points = np.c_[
        pts[:, :2],
        np.full(len(pts), 0.01),
    ]

    sh_back_actor.mapper.dataset.points = np.c_[
        pts[:, 0],
        np.full(len(pts), 4.99),
        pts[:, 2],
    ]

    sh_left_actor.mapper.dataset.points = np.c_[
        np.full(len(pts), -4.99),
        pts[:, 1],
        pts[:, 2],
    ]

    # -------------------------------------
    # ORBIT KAMERA
    # -------------------------------------

    # plotter.camera.azimuth += 1.3

    # -------------------------------------
    # RENDER + FRAME WRITE
    # -------------------------------------

    plotter.render()

    plotter.write_frame()

# =========================================================
# ZATVARANJE
# =========================================================

plotter.close()

print("MP4 export gotov.")
