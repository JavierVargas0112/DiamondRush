import cv2
import numpy as np
import pyautogui
import pytesseract

# Ruta a tesseract.exe (ajusta según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def tomar_screenshot():
    screenshot = pyautogui.screenshot()
    # Convertir a formato OpenCV BGR
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def extraer_texto_de_area(imagen, bbox):
    """
    bbox = (x1, y1, x2, y2)
    """
    recorte = imagen[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    # Convertir a escala de grises para mejor OCR
    gris = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    # Opcional: mejorar contraste, binarización, etc. Aquí simple:
    texto = pytesseract.image_to_string(gris, config='--psm 7')  # psm 7 = una línea de texto
    return texto.strip()


img = tomar_screenshot()
    
# Cambia estas coordenadas para la zona donde aparece "LEVEL X"
bbox_level = (430, 250, 560, 310)  # Ejemplo: (x1, y1, x2, y2)
    
texto_detectado = extraer_texto_de_area(img, bbox_level)
print("Texto detectado:", texto_detectado)