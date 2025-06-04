import copy
from collections import deque
from Analisis_2a import obtener_matriz_y_conteo
import hashlib
from SeleniumController import move
import captu

# === BFS  simulación ===

img = captu.tomar_screenshot()
    
bbox_level = (440, 300, 560, 360)  # (x1, y1, x2, y2)
    
texto_detectado = captu.extraer_texto_de_area(img, bbox_level)
print("Texto detectado:", texto_detectado)

def grid_hash(grid):
    # Convierte la matriz en un string y calcula un hash
    return hashlib.sha1(str(grid).encode()).hexdigest()

def bfs_simulado(grid_original, start, objetivo, tiene_llave_ini):
    m, n = len(grid_original), len(grid_original[0])
    q = deque()
    visited = set()
    
    q.append((start[0], start[1], "", copy.deepcopy(grid_original), tiene_llave_ini))

    while q:
        x, y, path, grid, tiene_llave = q.popleft()

        state_id = (x, y, tiene_llave, grid_hash(grid))
        if state_id in visited:
            continue
        visited.add(state_id)

        if isinstance(objetivo, list):
            if grid[x][y] in objetivo:
                return x, y, path, grid, tiene_llave
        else:
            if grid[x][y] == objetivo:
                return x, y, path, grid, tiene_llave

        for dx, dy, move in [(-1,0,'U'),(1,0,'D'),(0,-1,'L'),(0,1,'R')]:
            nx, ny = x+dx, y+dy
            if not (0 <= nx < m and 0 <= ny < n):
                continue
            celda = grid[nx][ny]

            # --- Comportamiento de rocas y huecos ---
            if celda == 'R' or celda == 'RD':
                rx, ry = nx + dx, ny + dy
                # La roca no puede salir del tablero
                if not (0 <= rx < m and 0 <= ry < n):
                    continue
                celda_detras = grid[rx][ry]
                # Solo permite empujar si la celda detrás es transitable
                if celda_detras not in ('C', 'X', 'D'):
                    continue
                new_grid = copy.deepcopy(grid)
                # Empujar roca a camino
                if celda_detras == 'C':
                    new_grid[rx][ry] = 'R'
                    new_grid[nx][ny] = 'C'
                # Empujar roca a hueco
                elif celda_detras == 'X':
                    new_grid[rx][ry] = 'C'
                    new_grid[nx][ny] = 'C'
                # Empujar roca sobre diamante
                elif celda_detras == 'D':
                    new_grid[rx][ry] = 'RD'
                    new_grid[nx][ny] = 'C'
                new_grid[x][y] = 'C'
                # Recoger diamante
                if celda == 'RD' and 'D' not in [cell for row in new_grid for cell in row]:
                    return rx, ry, path + move, new_grid, tiene_llave
                q.append((nx, ny, path + move, new_grid, tiene_llave))
                continue

            if celda == 'X':
                continue  # No puede pasar por huecos

            # --- objetos intransitables ---
            if celda == 'P':
                continue
            if celda == 'S' and any('D' in fila for fila in grid):
                continue
            if celda == 'T' and not tiene_llave:
                continue

            new_grid = copy.deepcopy(grid)
            new_tiene_llave = tiene_llave

            # Simular efecto
            if celda == 'U':
                new_grid[nx][ny] = 'P'
            elif celda == 'K' and not tiene_llave:
                new_tiene_llave = True
                new_grid[nx][ny] = 'C'
            elif celda == 'T' and tiene_llave:
                new_tiene_llave = False
                new_grid[nx][ny] = 'C'

            q.append((nx, ny, path + move, new_grid, new_tiene_llave))

    return None

# === Funcion principal ===
def resolver_nivel(matriz_original):
    jugador = encontrar_jugador(matriz_original)
    if not jugador:
        print("Jugador no encontrado.")
        return ""

    stack = [(jugador, "", copy.deepcopy(matriz_original), False)]
    while stack:
        pos, camino, matriz, tiene_llave = stack.pop()

        # Buscar proximo diamante
        if any('D' in celda for fila in matriz for celda in fila):
            resultado = bfs_simulado(matriz, pos, ['D', 'RD'], tiene_llave)
        else:
            #salida 
            resultado = bfs_simulado(matriz, pos, 'S', tiene_llave)

        if resultado:
            nx, ny, nuevo_camino, nueva_matriz, nuevo_tiene_llave = resultado
            nuevo_total = camino + nuevo_camino
            if not any('D' in celda for fila in nueva_matriz for celda in fila):
                # Buscar salida
                final = bfs_simulado(nueva_matriz, (nx, ny), 'S', nuevo_tiene_llave)
                if final:
                    fx, fy, camino_salida, matriz_final, _ = final
                    print("Ruta completa:", nuevo_total + camino_salida)
                    imprimir_mapa(matriz_final)
                    return nuevo_total + camino_salida
            else:
                nueva_matriz[nx][ny] = 'C'
                stack.append(((nx, ny), nuevo_total, nueva_matriz, nuevo_tiene_llave))

    print("No se encontró solución.")
    return ""

# === funciones ===
def encontrar_jugador(grid):
    for i, fila in enumerate(grid):
        for j, val in enumerate(fila):
            if val == 'J':
                return (i, j)
    return None

def imprimir_mapa(matriz):
    print("\n=== MAPA VIRTUAL ===")
    for fila in matriz:
        print(" ".join(fila))

# === Ejecución ===

nivel = texto_detectado.strip().split()[-1] 
ruta = f"screenshot/{nivel}.png"
matriz, conteo, area = obtener_matriz_y_conteo(ruta)
# matriz = [
#     ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
#     ['C', 'C', 'C', 'C', 'J', 'C', 'C', 'C'],
#     ['C', 'R', 'D', 'D', 'C', 'C', 'C', 'C'],
#     ['B', 'P', 'P', 'Y', 'P', 'P', 'P', 'P'],
#     ['D', 'C', 'C', 'R', 'D', 'D', 'C', 'P'],
#     ['P', 'C', 'C', 'C', 'C', 'C', 'C', 'B'],
#     ['P', 'Y', 'P', 'P', 'P', 'P', 'P', 'P'],
#     ['C', 'C', 'P', 'C', 'C', 'D', 'C', 'C'],
#     ['C', 'C', 'C', 'C', 'C', 'C', 'D', 'C'],
#     ['C', 'P', 'C', 'P', 'C', 'P', 'Y', 'P'],
#     ['C', 'R', 'C', 'P', 'B', 'P', 'D', 'C'],
#     ['D', 'D', 'D', 'P', 'D', 'P', 'C', 'S'],
# ]
imprimir_mapa(matriz)
resultado = resolver_nivel(matriz)
move(resultado)