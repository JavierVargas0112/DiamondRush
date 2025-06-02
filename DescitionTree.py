matrizEjemplo = [
    ["camino", "camino", "pared", "pared", "pared", "pared", "pared", "pared"],
    ["camino", "camino",  "pared", "pared", "pared", "pared", "pared", "pared"],
    ["camino", "camino", "camino", "camino", "camino", "camino", "camino", "camino"],
    ["pared", "diamante", "pared", "jugador", "camino", "camino", "camino", "pared", "diamante", "pared"],
    ["pared", "diamante", "pared", "pared", "pared", "pared", "pared", "pared", "diamante", "pared"],
    ["pared", "diamante", "diamante", "diamante", "diamante", "diamante", "diamante", "diamante", "diamante", "pared"],
    ["pared", "pared", "pared", "pared", "pared", "pared", "pared", "pared", "pared", "pared"],
    ["pared", "diamante", "pared", "roca", "roca", "pared", "diamante", "pared", "diamante", "pared"],
    ["pared", "diamante", "pared", "pared", "pared", "pared", "diamante", "pared", "diamante", "pared"],
    ["pared", "diamante", "diamante", "diamante", "diamante", "diamante", "diamante", "diamante", "diamante", "pared"],
    ["pared", "pared", "pared", "pared", "pared", "pared", "pared", "pared", "pared", "pared"],
    ["pared", "diamante", "pared", "boton", "boton", "pared", "diamante", "pared", "diamante", "pared"],
    ["pared", "diamante", "pared", "pared", "pared", "pared", "diamante", "pared", "diamante", "pared"],
    ["pared", "diamante", "diamante", "diamante", "diamante", "diamante", "diamante", "diamante", "diamante", "pared"],
    ["pared", "pared", "pared", "pared", "pared", "pared", "pared", "pared", "pared", "pared"]
]

matrizEjemplo2 =[
    ["i","c","c"],
    ["c","p","c"],
    ["c","c","c"]

]

class graph:
    def __init__(self, matrix):
        self.nodes = []
        self.edges = []
        self.start = None
        self.matrix = matrix
        self.nodeMatrix = []
        self.currentMatrix = nodeMatrix = []

        self.create_graph(matrix)
        

    def create_graph(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        # Crear todos los nodos y guardarlos en nodeMatrix
        self.nodeMatrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                
                    
                node = Node(name=matrix[i][j])
                if i == 0 and j == 0:
                    self.start = node  # Asignar el nodo inicial
                node.coordinates = (i, j)
                row.append(node)
                if node.name == "jugador":
                    self.start = node
            self.nodeMatrix.append(row)


        # Conectar nodos (no conecta paredes)
        for i in range(rows):
            for j in range(cols):
                node = self.nodeMatrix[i][j]
                if node.name == "p":
                    continue
                # Arriba
                if i > 0 and self.nodeMatrix[i-1][j].name != "p":
                    node.up = [self.nodeMatrix[i-1][j], True]
                # Abajo
                if i < rows-1 and self.nodeMatrix[i+1][j].name != "p":
                    node.down = [self.nodeMatrix[i+1][j], True]
                # Izquierda
                if j > 0 and self.nodeMatrix[i][j-1].name != "p":
                    node.left = [self.nodeMatrix[i][j-1], True]
                # Derecha
                if j < cols-1 and self.nodeMatrix[i][j+1].name != "p":
                    node.right = [self.nodeMatrix[i][j+1],True]
    
    
    
    def visualizar_nodematrix(self):
        for fila in self.nodeMatrix:
            print(" ".join([nodo.name[:3].ljust(3) for nodo in fila]))


class Node:
    # Arriba abajo, izquierda derecha tienen los nodos a los que se conecta y si se puede acceder a ellos
    def __init__(self,name ="", up = [None, None], down = [None, None], left=[None,None], right=[None,None]): 
        self.name = name
        self.coordinates = (0, 0)
        self.left = left
        self.right = right
        self.up = up
        self.down = down


class Player:
    def __init__(self, current, key=None, button=None):
        self.current = current 
        self.key = key
        self.button = button

    def mover_arriba(self):
        if self.current.up and self.current.up[0] and self.current.up[1]:
            self.current = self.current.up[0]
            print(f"Movido arriba a {self.current.coordinates}")
        else:
            print("No se puede mover arriba")

    def mover_abajo(self):
        if self.current.down and self.current.down[0] and self.current.down[1]:
            self.current = self.current.down[0]
            print(f"Movido abajo a {self.current.coordinates}")
        else:
            print("No se puede mover abajo")

    def mover_izquierda(self):
        if self.current.left and self.current.left[0] and self.current.left[1]:
            self.current = self.current.left[0]
            print(f"Movido izquierda a {self.current.coordinates}")
        else:
            print("No se puede mover a la izquierda")

    def mover_derecha(self):
        if self.current.right and self.current.right[0] and self.current.right[1]:
            self.current = self.current.right[0]
            print(f"Movido derecha a {self.current.coordinates}")
        else:
            print("No se puede mover a la derecha")
    
    from collections import deque

def BFS(grid, start_x, start_y):
    # Dimensiones de la grilla
    m = len(grid)
    n = len(grid[0])
    
    # Cola para BFS
    q = deque()
    q.append((start_x, start_y))
    
    # Matriz de visitados
    visited = [[False] * n for _ in range(m)]
    visited[start_x][start_y] = True
    
    # Direcciones de movimiento (arriba, abajo, izquierda, derecha)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    pared = "#"
    diamante = "B"
    final_x = 0
    final_y = 0
    found = False
    while q:
        x, y = q.popleft()
        
        # Explorar vecinos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Verificar límites y si el nodo no ha sido visitado
            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] != pared:
                 # Procesar el nodo actual
                found = True if grid[nx][ny] == diamante else False
                BuildPath(grid, x, y, dx, dy)
                visited[nx][ny] = True
                q.append((nx, ny))
                if found:
                    print(f"¡Diamante encontrado en: ({nx}, {ny})!")
                    final_x, final_y = nx, ny
                    break
    for row in grid:
      print("".join(row))
    print("Recorrido final:")
    finalPath = TrackPath(grid, final_x, final_y)
    print(f"Camino encontrado: {finalPath}")
                  

def TrackPath(grid, final_x, final_y):
  path = ""
  while grid[final_x][final_y] != "A":
   
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
   
def BuildPath(grid,x,y,dx,dy):
    nx, ny = x + dx, y + dy
    if dy!= 0:
        if dy > 0:
            grid[nx][ny] = "R"
        else:
            grid[nx][ny] = "L"
    else:
        if dx > 0:
            grid[nx][ny] = "D"
        else:
            grid[nx][ny] = "U"


    
    




def main():
    a = graph(matrizEjemplo2)
    print(a.visualizar_nodematrix())

    

    jugador = Player(a.start)
    jugador.mover_derecha()
    jugador.mover_izquierda() 



main()