from procesamiento import imprimir_mapa
from collections import deque
import copy

def flood_fill_info(matrizOriginal, inicio):
    matriz = copy.deepcopy(matrizOriginal)  # Hacemos una copia de la matriz original para no modificarla
    m, n = len(matriz), len(matriz[0])
    visitado = [[False]*n for _ in range(m)]
    stack = [inicio]
    hay_puerta = (-1,-1)
    hay_roca = (-1,-1)
    hay_boton = (-1,-1)



    while stack:
        x, y = stack.pop()
        if not (0 <= x < m and 0 <= y < n) or visitado[x][y]:
            continue
        visitado[x][y] = True
        celda = matriz[x][y]
        if celda == 'Y':
            hay_puerta = (x,y)
            continue  # Reconoce la puerta pero no la atraviesa
        if celda in ('R', 'RD'):
            hay_roca = (x,y)
        if celda == 'B':
            hay_boton = (x,y)
            continue  # Reconoce el botón pero no lo atraviesa
        # Solo expandimos por caminos transitables (no paredes, puertas ni botones)
        if celda in ('C', 'J', 'D', 'K', 'U', 'R'):
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                stack.append((nx, ny))

    return {
        'reja': hay_puerta,
        'roca': hay_roca,
        'boton': hay_boton
    }
    
def bfsSimpleToRock(gridOriginal, rockPosition, botonPosition):

    grid = copy.deepcopy(gridOriginal)
    """
    Realiza BFS desde la posición de la roca hasta el botón.
    Marca el camino en la matriz usando BuildPath y retorna el path usando TrackPath.
    """
    
    m, n = len(grid), len(grid[0])
    visitado = [[False]*n for _ in range(m)]
    prev = [[None]*n for _ in range(m)]
    queue = deque()
    rx, ry = rockPosition
    bx, by = botonPosition
    queue.append((rx, ry))
    visitado[rx][ry] = True

    # Direcciones: (dx, dy, letra)
    dirs = [(-1,0,'U'), (1,0,'D'), (0,-1,'L'), (0,1,'R')]

    while queue:
        x, y = queue.popleft()
        if (x, y) == (bx, by):
            break
        for dx, dy, move in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and not visitado[nx][ny]:
                # Solo caminos transitables para la roca
                if grid[nx][ny] in ('C', 'B','D'):
                    visitado[nx][ny] = True
                    prev[nx][ny] = (x, y, dx, dy)
                    BuildPath(grid, x, y, dx, dy)
                    queue.append((nx, ny))
    return TrackPath(grid, rx, ry, bx, by)

def bfsJugador(gridOriginal, start, goal):
    """
    Realiza BFS desde la posición del jugador (start) hasta goal.
    Retorna el string de movimientos para llegar al destino.
    """
    import copy
    from collections import deque

    grid = copy.deepcopy(gridOriginal)
    m, n = len(grid), len(grid[0])
    visitado = [[False]*n for _ in range(m)]
    prev = [[None]*n for _ in range(m)]
    queue = deque()
    sx, sy = start
    gx, gy = goal
    queue.append((sx, sy))
    visitado[sx][sy] = True

    dirs = [(-1,0,'U'), (1,0,'D'), (0,-1,'L'), (0,1,'R')]

    while queue:
        x, y = queue.popleft()
        if (x, y) == (gx, gy):
            break
        for dx, dy, move in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < m and 0 <= ny < n and not visitado[nx][ny]:
                # Solo caminos transitables para el jugador
                if grid[nx][ny] in ('C', 'D', 'B', 'Y', 'S'):  # Puedes ajustar según tus reglas
                    visitado[nx][ny] = True
                    prev[nx][ny] = (x, y, move)
                    queue.append((nx, ny))

    # Reconstruir el camino
    path = ""
    x, y = gx, gy
    while (x, y) != (sx, sy):
        if prev[x][y] is None:
            return ""  # No hay camino
        px, py, move = prev[x][y]
        path = move + path
        x, y = px, py
    return path

def BuildPath(grid, x, y, dx, dy):
    grid
    nx, ny = x + dx, y + dy
    if dy != 0:
        grid[nx][ny] = "R" if dy > 0 else "L"
    else:
        grid[nx][ny] = "D" if dx > 0 else "U"

def TrackPath(grid,roca_x,roca_y, boton_x, boton_y):
    """
    Reconstruye el string de pasos desde la posición final (final_x, final_y)
    hasta la posición inicial marcada con 'J', usando las marcas de dirección en la matriz.
    """
    path = ""
    x = boton_x
    y = boton_y
    while x != roca_x or y != roca_y:
        direction = grid[x][y]
        path = direction + path
        if direction == "U":
            x += 1
        elif direction == "D":
            x -= 1
        elif direction == "L":
            y += 1
        elif direction == "R":
            y -= 1
        else:
            break  # Por si acaso hay un error de marca
    return path

def checkIfNeedMoveRock(info):
    """
    Comprueba si los valores de 'reja', 'roca' y 'boton' en el diccionario info
    son todos diferentes a (-1, -1).
    """
    return all(info[k] != (-1, -1) for k in ['reja', 'roca', 'boton'])

def PositionToMoveRock(x, y, last_instruction):
    """
    Dada una posición (x, y) y una instrucción de dirección ('U', 'D', 'L', 'R'),
    retorna la posición anterior desde donde se empujó la roca (es decir, en sentido contrario).
    """
    if last_instruction == 'U':
        return x + 1, y
    elif last_instruction == 'D':
        return x - 1, y
    elif last_instruction == 'L':
        return x, y + 1
    elif last_instruction == 'R':
        return x, y - 1
    else:
        return x, y  # Si la instrucción no es válida, retorna la misma posición

def moveRockAndPlayer(grid, rockPosition, playerPosition, move):
    """
    Mueve la roca y el jugador según la dirección indicada por 'move'.
    Retorna las nuevas posiciones de la roca y el jugador.
    """
    dx, dy = 0, 0
    if move == 'U':
        dx, dy = -1, 0
    elif move == 'D':
        dx, dy = 1, 0
    elif move == 'L':
        dx, dy = 0, -1
    elif move == 'R':
        dx, dy = 0, 1

    # Nueva posición de la roca
    new_rock_x = rockPosition[0] + dx
    new_rock_y = rockPosition[1] + dy

    # Nueva posición del jugador
    new_player_x = playerPosition[0] + dx
    new_player_y = playerPosition[1] + dy

    # Actualizar la matriz
    grid[new_rock_x][new_rock_y] = 'R'  # Roca en nueva posición
    grid[rockPosition[0]][rockPosition[1]] = 'C'  # Celda vacía donde estaba la roca
    grid[new_player_x][new_player_y] = 'J'  # Jugador en nueva posición
    grid[playerPosition[0]][playerPosition[1]] = 'C'

    return (new_rock_x, new_rock_y), (new_player_x, new_player_y)
matriz = [
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C'],
    ['C', 'C', 'D', 'D', 'C', 'C', 'C', 'C'],
    ['P', 'P', 'P', 'C', 'P', 'P', 'P', 'P'],
    ['D', 'C', 'C', 'C', 'D', 'D', 'C', 'P'],
    ['P', 'C', 'C', 'C', 'C', 'C', 'C', 'P'],
    ['P', 'C', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['C', 'C', 'P', 'C', 'C', 'D', 'C', 'C'],
    ['C', 'C', 'C', 'C', 'C', 'C', 'D', 'C'],
    ['C', 'P', 'C', 'P', 'C', 'P', 'Y', 'P'],
    ['C', 'R', 'C', 'P', 'B', 'P', 'D', 'C'],
    ['D', 'D', 'D', 'P', 'D', 'P', 'C', 'S'],
]


# matriz = [
#     ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
#     ['C', 'C', 'C', 'C', 'J', 'C', 'C', 'C'],
#     ['C', 'R', 'D', 'D', 'C', 'C', 'C', 'C'],
#     ['B', 'P', 'P', 'Y', 'P', 'P', 'P', 'P'],
# ]
camino = ""
currentPosition = (6, 1)  # Posición del jugador
r = flood_fill_info(matriz, currentPosition)  # Inicia desde la posición del jugador (1, 4)
checkResult = checkIfNeedMoveRock(r)  # Verifica si es necesario mover la roca

if checkResult:
  pathRock = bfsSimpleToRock(matriz,r['roca'], r['boton'])
  if pathRock != "":
      currentPositionRock = r['roca']
      for move in pathRock:
          to_move_rock_x, to_move_rock_y = PositionToMoveRock(currentPositionRock[0], currentPositionRock[1], move)
          path_new_position_player = bfsJugador(matriz, currentPosition,( to_move_rock_x, to_move_rock_y))
          currentPosition =( to_move_rock_x, to_move_rock_y)
        

          camino += path_new_position_player

          #MOVER JUGADOR Y ROCA (BORRAR LUEGO)
          currentPositionRock,currentPosition = moveRockAndPlayer(matriz, currentPositionRock, currentPosition, move)
          
          camino += move
          print("Camino hasta ahora:", camino)
      matriz[currentPositionRock[0]][currentPositionRock[1]] = 'P'  
      print("matriz final")
      imprimir_mapa(matriz)

          

print(r)  