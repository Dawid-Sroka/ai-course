input_file = open("zad_input.txt", 'r')
output_file = open("zad_output.txt", 'w')
input_lines = [line.strip('\n') for line in input_file.readlines()]

board = [[char for char in line] for line in input_lines]

print(board)
no_rows = len(input_lines)
no_cols = len(input_lines[0])

print(input_lines)
print(no_rows)
print(no_cols)

initial = set()

class State:
    def __init__(self, positions):
        self.positions = positions
        self.visited = False

    def dump(self):
        print(self.positions)
        print(self.visited)

for i in range(no_rows):
    for j in range(no_cols):
        if board[i][j] == 'S':
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

def move_state(state: State, direction: str):
    newset = set()
    for pos in state.positions:
        newset.add( move(pos, direction) )
    
    new = State(frozenset(newset))
    return new

def check_goal(state: State):
    for pos in state.positions:
        i,j = pos
        if board[i][j] != 'G':
            return False
    return True

root = State(initial)
root.visited = True

root.dump()
node = move_state(root, 'L')
node.dump()

visited = set()
Q = []
visited.add(root.positions)
Q.append(root)
while len(Q) > 0:
    s = Q.pop(0)
    s.dump()
    if check_goal(s) == True:
        print("finished")
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

