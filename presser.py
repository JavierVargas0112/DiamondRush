import pyautogui
import keyboard
import time

sequence = 'UUDDLRLR'
key_map = {
    'U': 'up',
    'D': 'down',
    'L': 'left',
    'R': 'right'
}

print("Enfoca el juego en tu navegador, y presiona 'q' para comenzar la secuencia...")
keyboard.wait('q')

print("Iniciando secuencia...")
for char in sequence:
    key = key_map.get(char.upper())
    if key:
        pyautogui.press(key)
        print(f"Presionado: {key}")
        time.sleep(1)
    else:
        print(f"Carácter inválido: {char}")
