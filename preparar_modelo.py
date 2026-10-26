"""Prepara un modelo escaneado para la web: tamaño real, centrado y textura más ligera.

Uso: uv run --with trimesh --with pillow --with scipy preparar_modelo.py ENTRADA.glb SALIDA.glb LARGO_EN_METROS [LADO_TEXTURA]
Deja la máquina en metros, apoyada en el suelo (y = 0), centrada y con lo largo
a lo largo del eje X, con la punta de la espada hacia +X.
"""
import io
import sys

import numpy as np
import trimesh
from PIL import Image

entrada, salida, largo = sys.argv[1], sys.argv[2], float(sys.argv[3])
LADO_TEXTURA = int(sys.argv[4]) if len(sys.argv) > 4 else 2048

malla = trimesh.load(entrada).to_geometry()

# Lo largo, al eje X
ejes = np.argsort(malla.extents)[::-1]
if ejes[0] == 2:
    malla.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
elif ejes[0] == 1:
    malla.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1]))

# La punta de la espada es el extremo más estrecho: que quede en +X
v = malla.vertices
xmin, xmax = v[:, 0].min(), v[:, 0].max()
tramo = (xmax - xmin) * 0.1
alto_min = np.ptp(v[v[:, 0] < xmin + tramo][:, 1])
alto_max = np.ptp(v[v[:, 0] > xmax - tramo][:, 1])
if alto_min < alto_max:
    malla.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [0, 1, 0]))

# Tamaño real, centrada y en el suelo
malla.apply_scale(largo / malla.extents[0])
b = malla.bounds
malla.apply_translation([-(b[0][0] + b[1][0]) / 2, -b[0][1], -(b[0][2] + b[1][2]) / 2])

# Textura a 2K en JPEG
mat = malla.visual.material
tex = mat.baseColorTexture.convert("RGB").resize((LADO_TEXTURA, LADO_TEXTURA), Image.LANCZOS)
buf = io.BytesIO()
tex.save(buf, format="JPEG", quality=85)
mat.baseColorTexture = Image.open(io.BytesIO(buf.getvalue()))

malla.export(salida)
print(salida, "medidas (m):", np.round(malla.extents, 3))
