from PIL import Image
import os

# Ruta de la imagen grande (captura de pantalla completa)
ruta_imagen = "captura_juego.png"  # Cambia esto al nombre real si es diferente

# Coordenadas detectadas previamente del recorte del juego (actualiza si cambian)
top_left = (726, 309)
bottom_right = (1154, 947)

# Parámetros de la grilla
columnas = 15
filas = 10

# Crear carpeta para guardar baldosas
output_folder = "baldosas"
os.makedirs(output_folder, exist_ok=True)

# Cargar imagen completa
imagen = Image.open(ruta_imagen)

# Recortar sección del juego
juego = imagen.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))

# Tamaño de cada baldosa
ancho_baldosa = juego.width // columnas
alto_baldosa = juego.height // filas

# Recortar y guardar cada baldosa
for fila in range(filas):
    for col in range(columnas):
        izquierda = col * ancho_baldosa
        arriba = fila * alto_baldosa
        derecha = izquierda + ancho_baldosa
        abajo = arriba + alto_baldosa

        baldosa = juego.crop((izquierda, arriba, derecha, abajo))
        nombre_archivo = f"{output_folder}/baldosa_{fila}_{col}.png"
        baldosa.save(nombre_archivo)

print("✅ Baldosas guardadas en la carpeta 'baldosas'.")
