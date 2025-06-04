
import keyboard
import pydirectinput
import time

def move(sequence):
# Secuencia y mapeo
    
    key_map = {
        'U': 'up',
        'D': 'down',
        'L': 'left',
        'R': 'right'
    }

    print("Enfoca el juego en el navegador y presiona 'q' para comenzar la secuencia...")
    keyboard.wait('q')  # Espera hasta que se presione 'q'

    print("Iniciando secuencia...")
    time.sleep(1)  # Da tiempo para enfocar el juego

    for char in sequence:
        key = key_map.get(char.upper())
        if key:
            pydirectinput.press(key)
            print(f"Presionado: {key}")
            time.sleep(0.0)
        else:
            print(f"Carácter inválido: {char}")

    print("Secuencia completada. Manteniendo el navegador abierto...")
    input("Presiona Enter para cerrar...")