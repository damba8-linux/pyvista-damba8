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

# --- 2. PLOTTER ---
plotter = pv.Plotter()

# TRIK 1: Umjesto lightkita, koristimo 'headlight' koji je uvijek
# pričvršćen za kameru i osvjetljava točno ono što gledaš.
# To će "ubiti" crne sjene u rupama jer kamera tamo sada "vidi" svjetlo.
plotter.enable_lightkit()

# --- 3. LUKSUZNO ZLATO (PBR Fix za sjene) ---
plotter.add_mesh(
    grid_surface,
    color="#D4AF37",
    pbr=True,
    metallic=1.0,
    roughness=0.4,  # Povećano da površina postane "mat", što posvjetljuje sjene
    # TRIK 2: Pošto PBR ignorira ambient, koristimo visoki diffuse.
    # To omogućuje materijalu da "upije" i rasprši više svjetla u sjenama.
    diffuse=1.0,
    smooth_shading=True,
    show_scalar_bar=False,
)

# Parametarske crte
plotter.add_mesh(
    grid_surface,
    style="wireframe",
    color="#222222",
    line_width=1,
    opacity=0.1,
)

# --- 4. TRIK 3: DODATNO "FILL" SVJETLO (Sivkaste sjene) ---
# Dodajemo svjetlo koje je namjerno slabo i bijelo,
# postavljeno "iza" objekta da osvijetli rubove i dubine.
fill_light = pv.Light(position=(0, 0, -10), intensity=0.5, color="white")
plotter.add_light(fill_light)

# --- 5. OKVIR I POZADINA ---
plotter.show_grid(color="#555555", location="outer")
plotter.set_background("#222222", top="#444444")
# --- 6. KAMERA ---
plotter.camera_position = [(11, -11, 7), (0, 0, 2), (0, 0, 1)]
plotter.camera.zoom(1.7)

print("PBR je aktivan, ali smo 'napunili' sjene svjetlom.")
plotter.show()
