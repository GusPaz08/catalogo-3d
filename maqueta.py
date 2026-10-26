"""Maqueta provisional de una motosierra en 3D (GLB, en metros y a tamaño real).

Sirve solo para probar el visor y la realidad aumentada hasta tener
el escaneo de una máquina de verdad. Uso: uv run --with trimesh maqueta.py
"""
from pathlib import Path

import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.visual import TextureVisuals

NARANJA = [238, 106, 18, 255]
BLANCO = [232, 230, 226, 255]
NEGRO = [32, 33, 36, 255]
ACERO = [170, 174, 180, 255]
CADENA = [70, 72, 76, 255]


def pieza(malla, color, metal=0.0, rugosidad=0.6):
    malla.visual = TextureVisuals(
        material=PBRMaterial(baseColorFactor=color, metallicFactor=metal, roughnessFactor=rugosidad)
    )
    return malla


def caja(tam, centro, color, **kw):
    m = trimesh.creation.box(extents=tam)
    m.apply_translation(centro)
    return pieza(m, color, **kw)


def cilindro(radio, alto, centro, eje, color, **kw):
    m = trimesh.creation.cylinder(radius=radio, height=alto, sections=40)
    if eje == "x":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    elif eje == "y":
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    m.apply_translation(centro)
    return pieza(m, color, **kw)


escena = trimesh.Scene()
partes = {
    "carcasa": caja([0.30, 0.20, 0.18], [0.0, 0.12, 0.0], NARANJA, rugosidad=0.5),
    "tapa": caja([0.22, 0.05, 0.16], [-0.01, 0.245, 0.0], BLANCO, rugosidad=0.5),
    "empunadura_trasera": caja([0.15, 0.035, 0.04], [-0.235, 0.215, 0.0], NEGRO),
    "soporte_trasero": caja([0.03, 0.17, 0.04], [-0.30, 0.13, 0.0], NEGRO),
    "base_trasera": caja([0.16, 0.03, 0.05], [-0.23, 0.045, 0.0], NEGRO),
    "freno_cadena": caja([0.012, 0.13, 0.17], [0.165, 0.245, 0.0], NEGRO),
    "espada": caja([0.38, 0.058, 0.012], [0.34, 0.08, 0.0], ACERO, metal=0.8, rugosidad=0.35),
    "punta": cilindro(0.029, 0.012, [0.53, 0.08, 0.0], "z", ACERO, metal=0.8, rugosidad=0.35),
    "cadena": caja([0.39, 0.072, 0.008], [0.34, 0.08, 0.0], CADENA, metal=0.6, rugosidad=0.5),
    "tapon_combustible": cilindro(0.022, 0.016, [-0.06, 0.10, 0.098], "z", NEGRO),
    "arranque": caja([0.05, 0.025, 0.03], [-0.13, 0.29, 0.06], NEGRO),
}
asa = trimesh.creation.torus(major_radius=0.12, minor_radius=0.014)
asa.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
asa.apply_translation([0.10, 0.17, 0.0])
partes["asa_delantera"] = pieza(asa, NEGRO)

for nombre, malla in partes.items():
    escena.add_geometry(malla, node_name=nombre)

salida = Path(__file__).parent / "modelos" / "motosierra-maqueta.glb"
escena.export(salida)
print(salida, f"{salida.stat().st_size / 1024:.0f} KB", "medidas (m):", np.round(escena.extents, 3))
