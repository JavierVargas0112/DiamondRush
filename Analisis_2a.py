import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import Counter
import os

# === General  ===
elements_path = "elements2"
GRID_COLS = 8
GRID_ROWS = 12
UMBRAL_SIMILITUD = 0.4

# Coordenadas reales usadas en clasificación
x1, y1 = 344, 314
x2, y2 = 770, 954
cell_width = (x2 - x1) // GRID_COLS
cell_height = (y2 - y1) // GRID_ROWS

# === Cargar imágenes de referencia clasificadas ===
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

# ===  Diccionario de letras para visualización ===
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

# === Clasificador por similitud ===
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

# ===  Función principal===
def obtener_matriz_y_conteo(ruta_screenshot):
    screenshot = Image.open(ruta_screenshot).convert("RGB")
    game_area = screenshot.crop((x1, y1, x2, y2))

    conteo = Counter()
    mapa_virtual = [['' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

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
            letra = tipo_a_letra.get(tipo, "?")
            mapa_virtual[row][col] = letra

    return mapa_virtual, conteo, game_area

# === Función para imprimir matriz ===
def imprimir_mapa(matriz):
    print("\n=== MAPA VIRTUAL ===")
    for fila in matriz:
        print(" ".join(fila))

# === Visualización ===
def mostrar_grid_imagen(game_area):
    fig, ax = plt.subplots(figsize=(6, 9))
    ax.imshow(game_area)
    for i in range(1, GRID_COLS):
        ax.axvline(i * cell_width, color='white', linewidth=0.5)
    for j in range(1, GRID_ROWS):
        ax.axhline(j * cell_height, color='white', linewidth=0.5)
    plt.axis("off")
    plt.title("Área de Juego con Cuadrícula")
    plt.show()

# === Pruebas =======

#matriz, conteo, area = obtener_matriz_y_conteo("screenshot/1.png")
#imprimir_mapa(matriz)
#print("\nConteo de objetos por tipo:")
# for tipo in sorted(conteo):
#     print(f" - {tipo}: {conteo[tipo]}")
# mostrar_grid_imagen(area)
# print(matriz)

