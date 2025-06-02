import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import Counter
import os

# === CONFIGURACIÓN ===
screenshot_path = "screenshot/1.png"
elements_path = "elements2"           
GRID_COLS = 8
GRID_ROWS = 12
UMBRAL_SIMILITUD = 0.4

# Coordenadas reales usadas en clasificación
x1, y1 = 344, 314  # esquina superior izquierda
x2, y2 = 770, 954  # esquina inferior derecha

# Cálculo real de tamaño de celdas
cell_width = (x2 - x1) // GRID_COLS
cell_height = (y2 - y1) // GRID_ROWS

# === 1. Cargar imagen y recortar área de juego ===
screenshot = Image.open(screenshot_path).convert("RGB")
game_area = screenshot.crop((x1, y1, x2, y2))

# === 2. Cargar imágenes de referencia clasificadas ===
referencias = {}
for tipo in os.listdir(elements_path):
    tipo_path = os.path.join(elements_path, tipo)
    if not os.path.isdir(tipo_path):
        continue
    referencias[tipo] = []
    for archivo in os.listdir(tipo_path):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            ref_img = Image.open(os.path.join(tipo_path, archivo)).convert("RGB").resize((cell_width, cell_height))
            ref_cv = cv2.cvtColor(np.array(ref_img), cv2.COLOR_RGB2BGR)
            referencias[tipo].append(ref_cv)

# === 3. Clasificador por similitud (template matching) ===
def match_cell(cell_img_cv):
    max_score = -1
    best_tipo = "otro"
    for tipo, lista_refs in referencias.items():
        for ref_cv in lista_refs:
            res = cv2.matchTemplate(cell_img_cv, ref_cv, cv2.TM_CCOEFF_NORMED)
            score = res[0][0]
            if score > max_score:
                max_score = score
                best_tipo = tipo
    return best_tipo if max_score >= UMBRAL_SIMILITUD else "otro"

# === 4. Analizar cada celda del área de juego ===
conteo = Counter()
coordenadas_tipo = []

for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        left = col * cell_width
        upper = row * cell_height
        right = left + cell_width
        lower = upper + cell_height
        cell = game_area.crop((left, upper, right, lower))
        cell_cv = cv2.cvtColor(np.array(cell), cv2.COLOR_RGB2BGR)
        tipo = match_cell(cell_cv)
        conteo[tipo] += 1
        coordenadas_tipo.append((row, col, tipo))

# === 5. Mostrar conteo por tipo ===
print("Conteo de objetos por tipo:")
for tipo in sorted(conteo):
    print(f" - {tipo}: {conteo[tipo]}")

# === 6. Imprimir mapa virtual ===
tipo_a_letra = {
    "jugador": "J",
    "roca": "R",
    "camino": "C",
    "pared": "P",
    "salida": "S",
    "boton": "B",
    "diamante": "D",
    "puas": "U",
    "puerta": "T",
    "lava": "L",
    "puerta_boton": "Y",
    "hueco": "X",
    "llave": "K",
    "otro": "?"
}

mapa_virtual = [['' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
for row, col, tipo in coordenadas_tipo:
    letra = tipo_a_letra.get(tipo, "?")
    mapa_virtual[row][col] = letra

def imprimir_mapa(matriz):
    print("\n=== MAPA VIRTUAL ===")
    for fila in matriz:
        print(" ".join(fila))

imprimir_mapa(mapa_virtual)

# === 7. Visualización opcional con cuadrícula ===
fig, ax = plt.subplots(figsize=(6, 9))
ax.imshow(game_area)
for i in range(1, GRID_COLS):
    ax.axvline(i * cell_width, color='white', linewidth=0.5)
for j in range(1, GRID_ROWS):
    ax.axhline(j * cell_height, color='white', linewidth=0.5)
plt.axis("off")
plt.title("Área de Juego con Cuadrícula")
plt.show()

