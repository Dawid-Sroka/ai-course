from random import sample, randrange
from functools import cache


input_file = open("zad_input.txt", 'r')
output_file = open("zad_output.txt", 'w')
input_lines = [line.strip('\n') for line in input_file.readlines()]

board = [[char for char in line] for line in input_lines]

no_rows = len(input_lines)
no_cols = len(input_lines[0])


initial = set()

class State:
    def __init__(self, positions):
        self.positions = positions
        self.visited = False
        self.moves_sequence = ''

    def dump(self):
        print(self.positions)
        print(self.moves_sequence)
        print(self.visited)

for i in range(no_rows):
    for j in range(no_cols):
        if board[i][j] in {'S', 'B'}:
            initial.add((i,j))

initial = frozenset(initial)

letters = 'LDRU'
ldru_table = [(0,-1),(1,0),(0,1),(-1,0)]

@cache
def move_indexed(position: tuple, direction: int):
    i, j = position
    xdelta = ldru_table[direction][0]
    ydelta = ldru_table[direction][1]
    if board[i + xdelta][j + ydelta] != '#':
        return (i + xdelta, j + ydelta)
    else:
        return position

# def move(position: tuple, direction: str):
#     i, j = position
#     if direction == 'R' and board[i][j+1] != '#':
#         return (i, j + 1)
#     if direction == 'L' and board[i][j-1] != '#':
#         return (i, j - 1)
#     if direction == 'D' and board[i+1][j] != '#':
#         return (i + 1, j)
#     if direction == 'U' and board[i-1][j] != '#':
#         return (i - 1, j)
#     else:
#         return position

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

root = State(initial)
root.visited = True
# root.dump()


state = root

steps = 20
initial_moves = [0]*steps+[1]*steps+[2]*steps+[3]*steps
initial_string = ''
for i in range(len(initial_moves)):
    state = move_state(state, initial_moves[i])
    initial_string += letters[initial_moves[i]]

state.moves_sequence = ''
# state.dump()

# state = State(frozenset({(8, 20)}))


visited = set()
Q = []
visited.add(state.positions)
Q.append(state)
def BFS():
    while len(Q) > 0:
        s = Q.pop(0)
        # s.dump()
        if check_goal(s) == True:
            print("finished")
            solution = initial_string + s.moves_sequence
            output_file.write(solution)
            print(solution)
            break
        new_node = move_state(s, 0)
        if new_node.positions not in visited:
            visited.add(new_node.positions)
            new_node.visited = True
            Q.append(new_node)
        new_node = move_state(s, 1)
        if new_node.positions not in visited:
            visited.add(new_node.positions)
            new_node.visited = True
            Q.append(new_node)
        new_node = move_state(s, 2)
        if new_node.positions not in visited:
            visited.add(new_node.positions)
            new_node.visited = True
            Q.append(new_node)
        new_node = move_state(s, 3)
        if new_node.positions not in visited:
            visited.add(new_node.positions)
            new_node.visited = True
            Q.append(new_node)

BFS()

