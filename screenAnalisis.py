import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from collections import Counter
import os

# === CONFIG ===
screenshot_path = "screenshot/screenshot.png"
recorte_path = "screenshot/capture.png"
elements_path = "elements"
GRID_COLS = 10
GRID_ROWS = 15

# === 1. Cargar imágenes ===
screenshot = Image.open(screenshot_path).convert("RGB")
recorte = Image.open(recorte_path).convert("RGB")

# Convertir a OpenCV (BGR)
screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
recorte_cv = cv2.cvtColor(np.array(recorte), cv2.COLOR_RGB2BGR)

# === 2. Encontrar la ubicación del recorte ===
result = cv2.matchTemplate(screenshot_cv, recorte_cv, cv2.TM_CCOEFF_NORMED)
_, _, _, max_loc = cv2.minMaxLoc(result)
x1, y1 = max_loc
x2, y2 = x1 + recorte.width, y1 + recorte.height

# === 3. Recortar la región del juego ===
game_area = screenshot.crop((x1, y1, x2, y2))

# === 4. Dividir en cuadrícula ===
cell_width = game_area.width // GRID_COLS  
cell_height = game_area.height // GRID_ROWS

# === 5. Cargar imágenes de referencia ===
elementos = {
    "boton": "Boton.png",
    "camino": "camino_1.png",
    "pared_1": "Pared_1.png",
    "pared_2": "Pared_2.png",
    "pared_3": "Pared_3.png",
    "pared_4": "Pared_4.png",
    "pared_5": "Pared_5.png",
    "salida": "exit.png",
    "jugador": "Jugador.png",
    "puas": "Puas.png",
    "puerta_boton": "Puerta_boton.png",
    "puerta": "Puerta.png",
    "roca": "Roca.png",
    "diamante": "Diamante.png"
}

referencias = {}
for nombre, archivo in elementos.items():
    ref_img = Image.open(os.path.join(elements_path, archivo)).convert("RGB").resize((cell_width, cell_height))
    referencias[nombre] = cv2.cvtColor(np.array(ref_img), cv2.COLOR_RGB2BGR)

# Agrupar paredes y puertas
paredes = ["pared_1", "pared_2", "pared_3", "pared_4", "pared_5"]
puertas = ["puerta", "puerta_boton"]

# === 6. Clasificador por similitud ===
def match_cell(cell_img_cv):
    max_score = -1
    best_match = None
    for nombre, ref_cv in referencias.items():
        res = cv2.matchTemplate(cell_img_cv, ref_cv, cv2.TM_CCOEFF_NORMED)
        score = res[0][0]
        if score > max_score:
            max_score = score
            best_match = nombre
    # Umbral para considerar un match válido
    if max_score < 0.4:
        return "otro"
    # Agrupar categorías
    if best_match in paredes:
        return "pared"
    if best_match in puertas:
        return "puerta"
    if best_match == "camino":
        return "camino"
    if best_match == "boton":
        return "boton"
    if best_match == "salida":
        return "salida"
    if best_match == "jugador":
        return "jugador"
    if best_match == "puas":
        return "puas"
    if best_match == "roca":
        return "roca"
    if best_match == "diamante":
        return "diamante"
    return "otro"

# === 7. Analizar celdas ===
conteo = Counter()
coordenadas_tipo = []  # Lista para guardar (row, col, tipo)
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

# === 8. Mostrar resultados ===
print("Conteo de objetos por tipo:")
for tipo in ["boton", "camino", "pared", "salida", "jugador", "puas", "puerta", "roca", "otro"]:
    print(f" - {tipo}: {conteo[tipo]}")

# Imprimir todas las coordenadas con el tipo detectado
print("\nCoordenadas y tipo detectado de cada celda:")
for row, col, tipo in coordenadas_tipo:
    print(f"Fila: {row}, Columna: {col}, Tipo: {tipo}")

# === 9. Visualizar cuadrícula (opcional) ===
fig, ax = plt.subplots(figsize=(6, 9))
ax.imshow(game_area)
for i in range(1, GRID_COLS):
    ax.axvline(i * cell_width, color='white', linewidth=0.5)
for j in range(1, GRID_ROWS):
    ax.axhline(j * cell_height, color='white', linewidth=0.5)
plt.axis("off")
plt.title("Área de Juego con Cuadrícula")
plt.show()

 
# === 10. (Opcional) Crear e imprimir mapa virtual con letras pa ver mejor ===

# Mapeo de tipo a letra
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
    "otro": "X"
}

# Inicializar matriz vacía
mapa_virtual = [['' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

# Rellenar matriz
for row, col, tipo in coordenadas_tipo:
    letra = tipo_a_letra.get(tipo, ".")
    mapa_virtual[row][col] = letra

# Función para imprimir
def imprimir_mapa(matriz):
    print("\n=== MAPA VIRTUAL ===")
    for fila in matriz:
        print(" ".join(fila))

# Imprimir mapa en consola
imprimir_mapa(mapa_virtual)
