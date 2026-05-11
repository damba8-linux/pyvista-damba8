# type: ignore
import numpy as np
import pyvista as pv

# --- 1. GEOMETRIJA ---
rho, zeta = 1, 1.3
u, v = np.mgrid[0:4:100j, 0 : 4 * np.pi : 100j]
denom = np.cosh((u - v * np.cos(zeta)) / (rho * np.sin(zeta)))
x = rho * np.sin(zeta) / denom * np.cos(v / rho)
y = rho * np.sin(zeta) / denom * np.sin(v / rho)
z = u - rho * np.sin(zeta) * np.tanh((u - v * np.cos(zeta)) / (rho * np.sin(zeta)))

grid_surface = pv.StructuredGrid(x, y, z)

# --- 2. NAPREDNA TEKSTURA (Fix za VTK Warn) ---
# Radimo malo kompleksniju teksturu koja simulira studio
img = np.zeros((256, 256, 3), dtype=np.uint8)
img[:, :, :] = [40, 40, 45]  # Tamna baza (sjene)
img[0:40, :, :] = [255, 250, 240]  # Jako gornje svjetlo

tex = pv.Texture(img)
tex.interpolate = True  # FIX: VTK sada neće psovati
tex.mipmap = True  # FIX: VTK sada neće psovati

# --- 3. PLOTTER ---
plotter = pv.Plotter()
plotter.set_environment_texture(tex)

# --- 4. REALISTIČNO ZLATO ---
plotter.add_mesh(
    grid_surface,
    color="#C5A028",  # Malo "teža", zagasitija boja zlata
    pbr=True,
    metallic=1.0,
    roughness=0.22,  # Sredina: ni ogledalo ni mat
    smooth_shading=True,
    show_scalar_bar=False,
)

# Suptilni wireframe (da ne vrišti)
plotter.add_mesh(
    grid_surface, style="wireframe", color="#111111", line_width=1, opacity=0.05
)

# --- 5. POZADINA (Vraćamo gradijent) ---
# Forsiramo gradijent da razbijemo crnilo
plotter.set_background(color="#101010", top="#3a3a45")
# Dodajemo i jedan suptilan pod (floor) da ploha ima kontekst
plotter.add_mesh(
    pv.Plane(center=(0, 0, -0.5), i_size=5, j_size=5),
    color="#151515",
    pbr=True,
    roughness=1.0,
)

# --- 6. OKVIR I KAMERA ---
plotter.show_grid(color="#555555", location="outer", xtitle="X", ytitle="Y", ztitle="Z")
plotter.camera_position = [(11, -11, 7), (0, 0, 2), (0, 0, 1)]
plotter.camera.zoom(1.7)

print("Sada bi zlato trebalo imati 'dubinu', a sjene 'mekoću' bez VTK upozorenja.")
plotter.show()
