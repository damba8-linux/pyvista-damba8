# type: ignore
import os

import numpy as np
import pyvista as pv

# --- 1. GEOMETRIJA (Dini) ---
rho, zeta = 1, 1.3
u, v = np.mgrid[0:4:100j, 0 : 4 * np.pi : 100j]
denom = np.cosh((u - v * np.cos(zeta)) / (rho * np.sin(zeta)))
x = rho * np.sin(zeta) / denom * np.cos(v / rho)
y = rho * np.sin(zeta) / denom * np.sin(v / rho)
z = u - rho * np.sin(zeta) * np.tanh((u - v * np.cos(zeta)) / (rho * np.sin(zeta)))
grid_surface = pv.StructuredGrid(x, y, z)

# --- 2. PLOTTER ---
# Isključujemo sva defaultna svjetla da imamo potpunu kontrolu
plotter = pv.Plotter(lighting=None)
plotter.set_background(color="#0a1a2a", top="#000000")

# --- 3. RUČNA SVJETLA (Umjesto Light Kita) ---
# 1. Glavno svjetlo (Headlight) - prati kameru i daje sjaj zlatu
headlight = pv.Light(light_type="headlight", intensity=0.2)
plotter.add_light(headlight)

# 2. Ambijentalno svjetlo (Popunjava sjene da nisu skroz crne)
# Umjesto SetAmbientColor, dodajemo fiksno svjetlo koje ne baca jake sjene
ambient_light = pv.Light(position=(10, -10, 15), intensity=0.8)
plotter.add_light(ambient_light)

# --- 3. HDR ---
hdr_path = "venice_sunset_1k.hdr"
if os.path.exists(hdr_path):
    tex = pv.read_texture(hdr_path)
    tex.interpolate = True
    tex.mipmap = True
    plotter.set_environment_texture(tex)
    try:
        plotter.renderer.SetEnvironmentEmphasis(2.2)
    except Exception:
        pass

# --- 4. ZLATNA PLOHA + MREŽA ---
plotter.add_mesh(
    grid_surface,
    color="#FFD700",
    pbr=True,
    metallic=0.9,
    roughness=0.15,
    smooth_shading=True,
)

mesh_actor = plotter.add_mesh(
    grid_surface, style="wireframe", color="#102a43", line_width=1, opacity=0.08
)
mesh_actor.mapper.SetResolveCoincidentTopologyToPolygonOffset()
mesh_actor.mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-3.0, -3.0)

# --- 5. SJAJNE KOORDINATNE RAVNINE (PBR Floors) ---
# Uzimamo granice objekta da znamo gdje postaviti ravnine
bounds = grid_surface.bounds  # [xmin, xmax, ymin, ymax, zmin, zmax]

# Kreiramo tri tanke plohe (poda i zidova)
# Pod (XY ravnina)
floor_xy = pv.Plane(center=(0, 0, bounds[4]), direction=(0, 0, 1), i_size=4, j_size=4)
# Stražnji zidovi
wall_yz = pv.Plane(center=(bounds[0], 0, 1.7), direction=(1, 0, 0), i_size=4, j_size=4)
wall_xz = pv.Plane(center=(0, bounds[3], 1.7), direction=(0, 1, 0), i_size=4, j_size=4)

# Dodajemo ih s PBR efektom (Gunmetal siva koja se sjaji)
pbr_floor_args = dict(
    pbr=True,
    metallic=1.0,
    roughness=0.2,  # Malo glađe od zlata za jači odsjaj
    color="#2c3e50",  # Tamna metalik plavo-siva
    opacity=0.85,  # Polu-prozirno da se vidi gradijent pozadine
)

plotter.add_mesh(floor_xy, **pbr_floor_args)  # type: ignore[reportArgumentType]
plotter.add_mesh(wall_yz, **pbr_floor_args)  # type: ignore[reportArgumentType]
plotter.add_mesh(wall_xz, **pbr_floor_args)  # type: ignore[reportArgumentType]

# Dodajemo i tanki wireframe na te ravnine da zadržimo osjećaj grida
plotter.add_mesh(floor_xy, style="wireframe", color="#00f2ff", opacity=0.2)
plotter.add_mesh(wall_yz, style="wireframe", color="#00f2ff", opacity=0.2)
plotter.add_mesh(wall_xz, style="wireframe", color="#00f2ff", opacity=0.2)

# --- DODATAK: PROJEKCIJE (SJENE) NA RAVNINE ---

# 1. Projekcija na POD (Z-projekcija)
proj_z = grid_surface.copy()
proj_z.points[:, 2] = bounds[4]  # type: ignore[reportArgumentType]  # Svi Z bodovi idu na dno

# 2. Projekcija na LIJEVI ZID (X-projekcija)
proj_x = grid_surface.copy()
proj_x.points[:, 0] = bounds[0]  # type: ignore[reportArgumentType]  # Svi X bodovi idu na lijevu granicu

# 3. Projekcija na DESNI ZID (Y-projekcija)
proj_y = grid_surface.copy()
proj_y.points[:, 1] = bounds[3]  # type: ignore[reportArgumentType]  # Svi Y bodovi idu na stražnju granicu

# Dodajemo projekcije kao tamne, polu-prozirne plohe (bez PBR-a da ne blješte previše)
proj_args = dict(color="#102a43", opacity=0.3, show_scalar_bar=False)

plotter.add_mesh(proj_z, **proj_args)
plotter.add_mesh(proj_x, **proj_args)
plotter.add_mesh(proj_y, **proj_args)

# --- 6. KAMERA ---
plotter.camera_position = [(11, -11, 7), (0, 0, 2), (0, 0, 1)]
plotter.camera.zoom(1.6)

print("Svemirsko zlato na sjajnim metalik ravninama. To je to!")
plotter.show()

# # Definiraj ime datoteke
# html_file = "dini_surface_vizualizacija.html"
# # Exportaj scenu
# # backend='vtkjs' je standardni i najstabilniji za interaktivni prikaz
# plotter.export_html(html_file)
# print(f"Gotovo! Otvori datoteku '{html_file}' u svom pregledniku.")

# --- 8. FINALNI GLTF EXPORT ---
# Prvo instaliraj: pip install pygltflib
