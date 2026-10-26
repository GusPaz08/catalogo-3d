# Catálogo 3D · demo

Ficha de producto en 3D y realidad aumentada para tiendas de maquinaria de jardín: la máquina se gira con el dedo, se ven sus piezas y se pone a tamaño real con la cámara del móvil (iPhone y Android). Tiene un selector de calidad (1K, 2K o 4K), como en YouTube.

**Verla:** https://guspaz08.github.io/catalogo-3d/

- `index.html`: la página. Usa [model-viewer](https://modelviewer.dev) de Google (gratuito y de código abierto).
- `modelos/`: la motosierra en tres calidades (GLB, en metros y a tamaño real).
- `preparar_modelo.py`: deja un escaneo listo para la web. Lo pone a tamaño real, lo centra y aligera la textura: `uv run --with trimesh --with pillow --with scipy preparar_modelo.py entrada.glb salida.glb 0.55 2048`.
- `maqueta.py`: la maqueta de piezas simples que se usó antes de tener un escaneo.

## Créditos

Modelo de la motosierra: [«Chainsaw #3DST41»](https://sketchfab.com/3d-models/chainsaw-3dst41-23f2d98e2af84ad7816038dba61290e7), de mik.a., en Sketchfab, con licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es). Cambios: reescalado a tamaño real, centrado y con la textura reducida a 1K, 2K y 4K en JPEG.

Hecho por Gustavo Paz, dirigiendo a una IA: yo puse la idea, el criterio de tienda y la revisión.
