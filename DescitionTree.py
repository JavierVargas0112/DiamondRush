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

    
    




def main():
    a = graph(matrizEjemplo2)
    print(a.visualizar_nodematrix())

    

    jugador = Player(a.start)
    jugador.mover_derecha()
    jugador.mover_izquierda() 



main()