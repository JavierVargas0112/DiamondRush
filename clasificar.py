import os 
import cv2
import numpy as np
from PIL import Image

# Configuración
screenshot_path = "screenshot/8.png"
output_dir = "elements2"
GRID_COLS = 8
GRID_ROWS = 12

# Coordenadas del área de juego
x1, y1 = 344, 314  # esquina superior izquierda
x2, y2 = 770, 954  # esquina inferior derecha

# Categorías y teclas
categorias = ["camino", "pared", "jugador", "llave", "boton", "salida", "puas", "puerta", "roca", "diamante", "hueco", "puerta_boton", "lava"]
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
    'y': "puerta_boton",
    'x': "hueco",
    'l': "lava",
    'k': "llave",
    'q': "salir"
}

# Crear carpetas si no existen
for cat in categorias:
    cat_dir = os.path.join(output_dir, cat)
    os.makedirs(cat_dir, exist_ok=True)

# Función para obtener nombre de archivo
def obtener_siguiente_nombre_seguro(cat_dir, cat):
    i = 0
    while True:
        nombre = f"{cat}_{i:04}.png"
        ruta_completa = os.path.join(cat_dir, nombre)
        if not os.path.exists(ruta_completa):
            return nombre
        i += 1

# Cargar y recortar el área del juego
screenshot = Image.open(screenshot_path).convert("RGB")
game_area = screenshot.crop((x1, y1, x2, y2))

# Calcular tamaño de cada tile
cell_width = game_area.width // GRID_COLS
cell_height = game_area.height // GRID_ROWS

# Instrucciones
print("Instrucciones:")
for tecla, cat in tecla_a_categoria.items():
    if cat != "salir":
        print(f" - Presiona '{tecla}' para guardar como '{cat}'")
print(" - Presiona 'q' para salir")

# Clasificación manual
for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        left = col * cell_width
        upper = row * cell_height
        right = left + cell_width
        lower = upper + cell_height
        tile = game_area.crop((left, upper, right, lower))
        tile_cv = cv2.cvtColor(np.array(tile), cv2.COLOR_RGB2BGR)

        # Mostrar tile y esperar tecla
        cv2.imshow("Tile", tile_cv)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            print("Clasificación terminada.")
            cv2.destroyAllWindows()
            exit()
        elif chr(key) in tecla_a_categoria:
            cat = tecla_a_categoria[chr(key)]
            cat_dir = os.path.join(output_dir, cat)
            nombre_archivo = obtener_siguiente_nombre_seguro(cat_dir, cat)
            ruta = os.path.join(cat_dir, nombre_archivo)
            cv2.imwrite(ruta, tile_cv)
            print(f"Guardado en: {ruta}")
        else:
            print("Tecla no válida. Intenta de nuevo.")

cv2.destroyAllWindows()
