import cv2
import numpy as np
from PIL import Image
import os

# === CONFIGURACIÓN ===
screenshot_path = "screenshot/20.png"
elements_path = "elements2"
GRID_COLS = 8
GRID_ROWS = 12

# Coordenadas del área de juego
x1, y1 = 344, 314
x2, y2 = 770, 954

# Diccionario de teclas a categorías
tecla_a_categoria = {
    'c': "camino",
    'p': "pared",
    'j': "jugador",
    'b': "boton",
    's': "salida",
    'u': "puas",
    't': "puerta",
    'r': "roca",
    'd': "diamante",
    'x': "hueco",
    'y': "puerta_boton",
    'l': "lava",
    'k': "llave",
    'q': "salir"
}

# Crear carpetas si no existen
for cat in tecla_a_categoria.values():
    if cat != "salir":
        os.makedirs(os.path.join(elements_path, cat), exist_ok=True)

# === Cargar imagen y recortar área de juego ===
screenshot = Image.open(screenshot_path).convert("RGB")
game_area = screenshot.crop((x1, y1, x2, y2))

# Tamaño de celdas
cell_width = (x2 - x1) // GRID_COLS
cell_height = (y2 - y1) // GRID_ROWS

# === Clasificar una celda por letra ===
def clasificar_celda_manual_letra(fila, columna):
    row = fila - 1
    col = columna - 1

    if row < 0 or row >= GRID_ROWS or col < 0 or col >= GRID_COLS:
        print("❌ Coordenadas fuera del rango.")
        return

    # Recortar celda
    left = col * cell_width
    upper = row * cell_height
    right = left + cell_width
    lower = upper + cell_height
    cell = game_area.crop((left, upper, right, lower))
    cell_cv = cv2.cvtColor(np.array(cell), cv2.COLOR_RGB2BGR)

    # Mostrar instrucciones
    print(f"Clasificando celda ({fila}, {columna}). Presiona la tecla correspondiente:")
    for tecla, cat in tecla_a_categoria.items():
        if cat != "salir":
            print(f" - '{tecla}' para '{cat}'")
    print(" - 'q' para cancelar esta celda")

    # Mostrar celda
    cv2.imshow("Celda", cell_cv)
    key = cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()

    if chr(key) == 'q':
        print("❌ Clasificación cancelada.")
        return

    letra = chr(key)
    if letra in tecla_a_categoria:
        categoria = tecla_a_categoria[letra]
        carpeta_destino = os.path.join(elements_path, categoria)

        # Buscar un nombre de archivo no usado
        i = 0
        while True:
            filename = os.path.join(carpeta_destino, f"{categoria}_{i:04}.png")
            if not os.path.exists(filename):
                break
            i += 1

        cv2.imwrite(filename, cell_cv)
        print(f"✅ Celda guardada como '{filename}' en carpeta '{categoria}'")
    else:
        print("❌ Tecla no válida. Intenta de nuevo.")

# === USO ===
clasificar_celda_manual_letra(8, 1)  # fila, columna


