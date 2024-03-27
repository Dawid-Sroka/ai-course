from random import sample, randrange


input_file = open("zad_input.txt", 'r')
output_file = open("zad_output.txt", 'w')
input_lines = [line.strip('\n') for line in input_file.readlines()]

board = [[char for char in line] for line in input_lines]

# print(board)
no_rows = len(input_lines)
no_cols = len(input_lines[0])

# print(input_lines)
# print(no_rows)
# print(no_cols)

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

def move(position: tuple, direction: str):
    i, j = position
    if direction == 'R' and board[i][j+1] != '#':
        return (i, j + 1)
    if direction == 'L' and board[i][j-1] != '#':
        return (i, j - 1)
    if direction == 'D' and board[i+1][j] != '#':
        return (i + 1, j)
    if direction == 'U' and board[i-1][j] != '#':
        return (i - 1, j)
    else:
        return position

def move_state(state: State, direction: str) -> State:
    newset = set()
    for pos in state.positions:
        newset.add( move(pos, direction) )
    
    new = State(frozenset(newset))
    new.moves_sequence = state.moves_sequence + direction
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

# state = root
# random_len = 30
# moves = 'UDRL'
# for i in range(random_len):
#     k = randrange(4)
#     movex = moves[k]
#     print(movex)
#     state = move_state(state, movex)

#state.dump()
# node = move_state(state, 'L')
# node.dump()

state = root
steps = 20
initial_moves = 'L' * steps + 'D' * steps + 'R' * steps +  'U' * steps
initial_moves = initial_moves * 1
# unite_blk = 'L'*5 + 'D'*5
# escape_blk_left = 'LU'*5

# escape_blk_up = 'UR'*5

# # initial_moves = unite_blk+escape_blk_left+'L'* 5+ 'U'*5+escape_blk_up
# initial_moves = 'L' * steps + 'D' * steps

# # initial_moves = 'L' * 5 + 'D' * 5 + 'R' * steps +  'U' * steps



def greedy(s: State, sequence: str):
    for j in range(40):
        # s.dump()

        next_node = [0,0,0,0]
        next_node[0] = len(move_state(s, 'R').positions)
        next_node[1] = len(move_state(s, 'L').positions)
        next_node[2] = len(move_state(s, 'U').positions)
        next_node[3] = len(move_state(s, 'D').positions)

        minimal = 1000
        index = 0
        for i in range(4):
            if next_node[i] < minimal:
                minimal = next_node[i]
                index = i
        
        s = move_state(s, 'RLUD'[index])
        sequence = sequence + 'RLUD'[index]
    return s, sequence

seq = ''
state, seq = greedy(state, seq)
# print(seq)
initial_moves = seq

# for i in range(len(initial_moves)):
#     state = move_state(state, initial_moves[i])

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
            solution = initial_moves + s.moves_sequence
            output_file.write(solution)
            print(solution)
            break
        new_node = move_state(s, 'R')
        if new_node.positions not in visited:
            visited.add(new_node.positions)
            new_node.visited = True
            Q.append(new_node)
        new_node = move_state(s, 'L')
        if new_node.positions not in visited:
            visited.add(new_node.positions)
            new_node.visited = True
            Q.append(new_node)
        new_node = move_state(s, 'D')
        if new_node.positions not in visited:
            visited.add(new_node.positions)
            new_node.visited = True
            Q.append(new_node)
        new_node = move_state(s, 'U')
        if new_node.positions not in visited:
            visited.add(new_node.positions)
            new_node.visited = True
            Q.append(new_node)

BFS()

