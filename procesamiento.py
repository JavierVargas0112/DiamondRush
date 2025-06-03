from collections import deque
from Analisis_2a import obtener_matriz_y_conteo
import copy

# === BFS para encontrar el diamante 'D' ===
global tiene_llave
tiene_llave = False

def pisar_pua(grid, x, y):
    if grid[x][y] == 'U':
        grid[x][y] = 'P'
    return

def BuildPath(grid, x, y, dx, dy):
    nx, ny = x + dx, y + dy
    if dy != 0:
        grid[nx][ny] = "R" if dy > 0 else "L"
    else:
        grid[nx][ny] = "D" if dx > 0 else "U"

def TrackPath(grid, final_x, final_y):
    path = ""
    while grid[final_x][final_y] != "J":
        direction = grid[final_x][final_y]
        path = direction + path
        if direction == "U":
            final_x += 1
        elif direction == "D":
            final_x -= 1
        elif direction == "L":
            final_y += 1
        elif direction == "R":
            final_y -= 1
    return path


def BFS(grid, start_x, start_y, objetivo):
    global tiene_llave

    m, n = len(grid), len(grid[0])
    q = deque()
    path_grid = copy.deepcopy(grid)
    path_grid[start_x][start_y] = "J"
    q.append((start_x, start_y, path_grid))
    visited = set()

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # U, D, L, R

    while q:
        x, y, path_grid = q.popleft()

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < m and 0 <= ny < n):
                continue

            celda = grid[nx][ny]

            if celda == 'P':
                continue
            if celda == 'T' and tiene_llave == False:
                continue

            # Si pisa una púa
            pisar_pua(grid, nx, ny)

            # Si pisa una llave
            if celda == 'K' and tiene_llave == False:
                tiene_llave = True

                grid[nx][ny] = 'C'

            # Si pisa una puerta con llave
            if celda == 'T' and tiene_llave:
                tiene_llave = False
                grid[nx][ny] = 'C'

            estado = (nx, ny)
            if estado in visited:
                continue
            visited.add(estado)

            nuevo_path_grid = copy.deepcopy(path_grid)
            BuildPath(nuevo_path_grid, x, y, dx, dy)

            if celda == objetivo:
                camino = TrackPath(nuevo_path_grid, nx, ny)
                return (nx, ny, camino)

            q.append((nx, ny, nuevo_path_grid))

    return None


# ==================== logica

def encontrar_jugador(grid):
    for i, fila in enumerate(grid):
        for j, val in enumerate(fila):
            if val == 'J':
                return (i, j)
    return None

def resolver_diamantes_y_salida(grid):
    global tiene_llave
    tiene_llave = False

    recorrido_total = ""
    jugador_pos = encontrar_jugador(grid)
    if not jugador_pos:
        print("Jugador no encontrado.")
        return ""

    while True:
        resultado = BFS(grid, *jugador_pos, 'D')

        if not resultado:
            hay_diamante = any('D' in fila for fila in grid)
            hay_llave = any('K' in fila for fila in grid)
            if not hay_diamante:
                break
            if not hay_llave:
                print("No hay más caminos ni llaves.")
                break

            resultado_llave = BFS(grid, *jugador_pos, 'K')
            if not resultado_llave:
                print("No se puede acceder a ninguna llave.")
                break
            nx, ny, camino_k = resultado_llave
            recorrido_total += camino_k
            jugador_pos = (nx, ny)
            continue

        nx, ny, camino_d = resultado
        grid[nx][ny] = 'C'
        recorrido_total += camino_d
        jugador_pos = (nx, ny)

    # Ir a la salida
    if not any('D' in fila for fila in grid):
        resultado = BFS(grid, *jugador_pos, 'S')
        if resultado:
            nx, ny, camino_s = resultado
            recorrido_total += camino_s
        else:
            print("No se pudo llegar a la salida.")

    return recorrido_total



# ===============================
# USO
# ===============================
def imprimir_mapa(matriz):
    print("\n=== MAPA VIRTUAL ===")
    for fila in matriz:
        print(" ".join(fila))

nivel = 3
ruta = f"screenshot/{nivel}.png"
matriz, conteo, area = obtener_matriz_y_conteo(ruta)
imprimir_mapa(matriz)
camino_total = resolver_diamantes_y_salida(matriz)
print("Ruta completa:", camino_total)

imprimir_mapa(matriz)

#matriz=[['S','D','C','U','C','J'],
#        ['C','U','C','U','U','C']]
# ===============================
# PRUEBAS
# ===============================

# print("\nConteo de objetos por tipo:")
# for tipo in sorted(conteo):
#     print(f" - {tipo}: {conteo[tipo]}")
# imprimir_mapa(matriz)

#nomenclatura: 

# tipo_a_letra = {
#     "jugador": "J",
#     "roca": "R",
#     "camino": "C",
#     "pared": "P",
#     "salida": "S",
#     "boton": "B",
#     "diamante": "D",
#     "puas": "U",
#     "puerta": "T",
#     "lava": "L",
#     "puerta_boton": "Y",
#     "hueco": "X",
#     "llave": "K",
#     "otro": "?"
# }


