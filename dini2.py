# type: ignore
import numpy as np
import pyvista as pv

# --- 1. GEOMETRIJA (Dini's Surface) ---
rho, zeta = 1, 1.3
u, v = np.mgrid[0:4:100j, 0 : 4 * np.pi : 100j]

denom = np.cosh((u - v * np.cos(zeta)) / (rho * np.sin(zeta)))
x = rho * np.sin(zeta) / denom * np.cos(v / rho)
y = rho * np.sin(zeta) / denom * np.sin(v / rho)
z = u - rho * np.sin(zeta) * np.tanh((u - v * np.cos(zeta)) / (rho * np.sin(zeta)))

grid_surface = pv.StructuredGrid(x, y, z)
grid_surface["Visina"] = z.ravel(order="F")

# --- 2. INICIJALIZACIJA PLOTTERA ---
plotter = pv.Plotter(lighting="light_kit")

# Glavna ploha (Magma s efektom sjaja)
plotter.add_mesh(
    grid_surface,
    scalars="Visina",
    cmap="magma",
    smooth_shading=True,
    specular=0.8,
    show_scalar_bar=False,
    ambient=0.2,
)

# Parametarske crte (Fix za Z-fighting treperenje)
actor = plotter.add_mesh(
    grid_surface,
    style="wireframe",
    color="white",
    line_width=1,
    opacity=0.3,
)
# Force-amo da linije budu uvijek "ispred" plohe u memoriji grafičke
actor.mapper.SetResolveCoincidentTopologyToPolygonOffset()
actor.mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-1.0, -1.0)

# --- 3. SPOJENI KOORDINATNI SUSTAV (Box Grid) ---
# show_grid() automatski stvara ravnine koje su spojene po bridovima
plotter.show_grid(
    color="#00f2ff",  # Neon Cyan boja
    # grid_alpha=0.15,  # Suptilnost unutrašnje mreže
    location="outer",  # Grid se miče na stražnje ravnine pri rotaciji
    ticks="both",
    n_xlabels=5,
    n_ylabels=5,
    n_zlabels=5,
    xtitle="X-os",
    ytitle="Y-os",
    ztitle="Z-os",
    font_size=14,
)

# Outline (Čvrsti bridovi kaveza)
outline = grid_surface.outline()
plotter.add_mesh(outline, color="#00f2ff", line_width=2, opacity=0.6)

# --- 4. POZADINA I AMBIJENT ---
plotter.set_background("#000000", top="#0a0a20")  # type: ignore[reportArgumentType]
plotter.enable_anti_aliasing()

# --- 5. KAMERA (Fokus i Zoom) ---
# Gledamo u točku (0,0,2) jer je to sredina objekta po visini
plotter.camera_position = [(11, -11, 7), (0, 0, 2), (0, 0, 1)]
plotter.camera.zoom(1.6)

print("Lansiramo vizualizaciju...")
plotter.show()
