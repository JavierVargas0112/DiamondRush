from collections import deque
from Analisis_2a import obtener_matriz_y_conteo
import copy

# === Lógica de nodos y grafo ===

class Node:
    def __init__(self, name=None):
        self.name = name
        self.coordinates = ()
        self.left = None
        self.right = None
        self.up = None
        self.down = None

class graph:
    def __init__(self, matrix):
        self.matrix = matrix
        self.nodeMatrix = []
        self.start = None
        self.create_graph(matrix)

    def create_graph(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        self.nodeMatrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                valor = matrix[i][j]
                node = Node(name=valor)
                node.coordinates = (i, j)
                row.append(node)
                if valor == 'J':  # Jugador
                    self.start = node
            self.nodeMatrix.append(row)

        for i in range(rows):
            for j in range(cols):
                node = self.nodeMatrix[i][j]
                if node.name == 'P':  # Pared: no conecta
                    continue
                if i > 0 and self.nodeMatrix[i-1][j].name != 'P':
                    node.up = [self.nodeMatrix[i-1][j], True]
                if i < rows-1 and self.nodeMatrix[i+1][j].name != 'P':
                    node.down = [self.nodeMatrix[i+1][j], True]
                if j > 0 and self.nodeMatrix[i][j-1].name != 'P':
                    node.left = [self.nodeMatrix[i][j-1], True]
                if j < cols-1 and self.nodeMatrix[i][j+1].name != 'P':
                    node.right = [self.nodeMatrix[i][j+1], True]

    def visualizar_nodematrix(self):
        for fila in self.nodeMatrix:
            print(" ".join([nodo.name for nodo in fila]))

class Player:
    def __init__(self, nodoActual):
        self.nodoActual = nodoActual

    def ir(self, direccion):
        if direccion == "arriba" and self.nodoActual.up and self.nodoActual.up[1]:
            self.nodoActual = self.nodoActual.up[0]
            return True
        elif direccion == "abajo" and self.nodoActual.down and self.nodoActual.down[1]:
            self.nodoActual = self.nodoActual.down[0]
            return True
        elif direccion == "izquierda" and self.nodoActual.left and self.nodoActual.left[1]:
            self.nodoActual = self.nodoActual.left[0]
            return True
        elif direccion == "derecha" and self.nodoActual.right and self.nodoActual.right[1]:
            self.nodoActual = self.nodoActual.right[0]
            return True
        return False

    def obtenerNombre(self):
        return self.nodoActual.name

    def obtenerCoordenadas(self):
        return self.nodoActual.coordinates

# === BFS para encontrar el diamante 'D' ===

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
    m, n = len(grid), len(grid[0])
    q = deque()
    q.append((start_x, start_y))
    visited = [[False]*n for _ in range(m)]
    visited[start_x][start_y] = True
    path_grid = copy.deepcopy(grid)
    path_grid[start_x][start_y] = "J"  # Marca la posición inicial

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # U, D, L, R

    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] != 'P':
                visited[nx][ny] = True
                BuildPath(path_grid, x, y, dx, dy)
                q.append((nx, ny))
                if grid[nx][ny] == objetivo:
                    camino = TrackPath(path_grid, nx, ny)
                    return (nx, ny, camino)
    return None


# ===============================
# INICIALIZAR
# ===============================

nivel = 3  # Cambiar al nivel deseado
ruta = f"screenshot/{nivel}.png"
matriz, conteo, area = obtener_matriz_y_conteo(ruta)

# ===============================
# PRUEBAS
# ===============================

def imprimir_mapa(matriz):
    print("\n=== MAPA VIRTUAL ===")
    for fila in matriz:
        print(" ".join(fila))

print("\nConteo de objetos por tipo:")
for tipo in sorted(conteo):
    print(f" - {tipo}: {conteo[tipo]}")
imprimir_mapa(matriz)

a = graph(matriz)
print("Visualización del mapa:")
a.visualizar_nodematrix()

print("\nInicio del jugador en:", a.start.coordinates)
jugador = Player(a.start)

print("Nombre en posición inicial:", jugador.obtenerNombre())
print("Coordenadas:", jugador.obtenerCoordenadas())

print("\nMoviendo a la derecha...")
if jugador.ir("derecha"):
    print("Movimiento exitoso.")
else:
    print("Movimiento bloqueado.")
print("Nueva posición:", jugador.obtenerCoordenadas(), "-", jugador.obtenerNombre())

# ===============================
# Búsqueda completa paso a paso
# ===============================
coordenadas_actuales = a.start.coordinates
grid_original = copy.deepcopy(matriz)
recorrido_total = ""

# Buscar todos los diamantes
while True:
    resultado = BFS(matriz, *coordenadas_actuales, 'D')
    if not resultado:
        break
    nx, ny, camino = resultado
    recorrido_total += camino
    matriz[nx][ny] = 'C'  # Marcar como recogido
    coordenadas_actuales = (nx, ny)

# Buscar la salida
resultado = BFS(matriz, *coordenadas_actuales, 'S')
if resultado:
    nx, ny, camino = resultado
    recorrido_total += camino

# Mostrar camino total
print(recorrido_total)

