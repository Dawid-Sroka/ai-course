# Dawid Sroka, zad3 z pracowni 2
#
# Algorytm A*
# Mając dany stan S = {p1,p2,...,pk}, czyli zbiór pozycji, wartość heurystyki
# wyliczam tak:
# dla każdej pozycji p znam minimalną liczbę ruchów k_p, której potrzebuje 
# komandos, żeby z p dostać się do jakiegoś punktu docelowego.
# Heurystyka dla stanu S to maksimum z k_p po wszystkich p należących do S.
#
# Wartości k_p tablicuję na początku dla wszystkich pozycji w labiryncie
# puszczając BFSa z każdego punktu docelowego (funkcja dist_from_goal).
# 
# Właściwy BFS w A* utrzymuje kolejkę FIFO, gdzie priorytet to para
# (koszt dotarcia do węzła (czyli liczba wykonanych ruchów) + heurystyka,
# ciąg wykonanych ruchów). 

from functools import cache
from queue import PriorityQueue

input_file = open("zad_input.txt", 'r')
output_file = open("zad_output.txt", 'w')
input_lines = [line.strip('\n') for line in input_file.readlines()]

board = [[char for char in line] for line in input_lines]
no_rows = len(input_lines)
no_cols = len(input_lines[0])

initial = set()
goals = set()

for i in range(no_rows):
    for j in range(no_cols):
        if board[i][j] in {'S', 'B'}:
            initial.add((i,j))
        if board[i][j] in {'G', 'B'}:
            goals.add((i,j))

class State:
    def __init__(self, positions):
        self.positions = positions
        self.moves_sequence = ''

    def dump(self):
        print(self.positions)
        print(self.moves_sequence)

letters = 'LDRU'
ldru_table = [(0,-1),(1,0),(0,1),(-1,0)]

@cache
def move_indexed(position: tuple, direction: int):
    i, j = position
    xdelta, ydelta = ldru_table[direction]
    if board[i + xdelta][j + ydelta] != '#':
        return (i + xdelta, j + ydelta)
    else:
        return position

def move_state(state: State, direction: int) -> State:
    newset = set()
    for pos in state.positions:
        newset.add( move_indexed(pos, direction) )
    
    new = State(frozenset(newset))
    new.moves_sequence = state.moves_sequence + letters[direction]
    return new

def check_goal(state: State):
    for pos in state.positions:
        i,j = pos
        if board[i][j] not in {'G', 'B'}:
            return False
    return True

closest_goal = [[1000 for x in range(no_cols)] for y in range(no_rows)]

def dist_from_goal(goal_pos):
    visited = set()
    Q = []
    visited.add(goal_pos)
    dist = 0
    closest_goal[goal_pos[0]][goal_pos[1]] = 0
    Q.append((dist,goal_pos))
    while len(Q) > 0:
        d, pos = Q.pop(0)
        i, j = pos
        for k in range(4):
            xdelta, ydelta = ldru_table[k]
            new_i, new_j = i + xdelta, j + ydelta
            if board[new_i][new_j] != '#' and (new_i, new_j) not in visited:
                visited.add((new_i, new_j))
                if d+1 < closest_goal[new_i][new_j]:
                    closest_goal[new_i][new_j] = d+1
                Q.append((d+1, (new_i,new_j)))

for goal in goals:
    dist_from_goal(goal)


def calc_priority(state: State):
    dists = [closest_goal[p[0]][p[1]] for p in state.positions]
    return len(state.moves_sequence)*1 + 1.0*max(dists)

initial = frozenset(initial)
root = State(initial)

visited = set()
pq = PriorityQueue()
pq.put((calc_priority(root), root.moves_sequence, root))

def BFS():
    while not pq.empty():
        p, mov_seq, s = pq.get()
        if s.positions in visited:
            continue
        visited.add(s.positions)

        if check_goal(s) == True:
            output_file.write(s.moves_sequence)
            break

        new_node = move_state(s, 0)
        pq.put((calc_priority(new_node), new_node.moves_sequence, new_node))
        new_node = move_state(s, 1)
        pq.put((calc_priority(new_node), new_node.moves_sequence, new_node))
        new_node = move_state(s, 2)
        pq.put((calc_priority(new_node), new_node.moves_sequence, new_node))
        new_node = move_state(s, 3)
        pq.put((calc_priority(new_node), new_node.moves_sequence, new_node))

BFS()
