# Dawid Sroka, zad1 z pracowni 3
#

from random import sample, randrange
from functools import cache
from queue import Queue
from copy import deepcopy
from operator import add


input_file = open("zad_input.txt", 'r')
output_file = open("zad_output.txt", 'w')
input_lines = input_file.readlines()

# Parse the input
no_rows, no_cols = [int(d) for d in input_lines[0].split()]
R = no_rows + no_cols
work_board = [[0 for x in range(no_cols)] for y in range(no_rows)]
x_arr = [[int(d) for d in l.split()] for l in input_lines[1:no_rows+1]]
y_arr = [[int(d) for d in l.split()] for l in input_lines[no_rows+1:]]

def dump(m):
    for i in range(no_rows):
        line = ""
        for j in range(no_cols):
            if m[i][j] == 1:
                line += "#"
            elif m[i][j] == -1:
                line += " "
            else:
                line += "?"
        print(line)
    print("")

def write_solution_to_output(m):
    output_file.seek(0, 0)
    for i in range(no_rows):
        line = ""
        for j in range(no_cols):
            if m[i][j] == 1:
                line += "#"
            else:
                line += "."
        output_file.write(line+"\n")

# ===============================================        

def generate_possible(dim:int, blocks: list[int]):
    possibles = set()
    prevs = ()
    iter_possible(dim, dim, blocks, possibles, prevs)
    return possibles

def iter_possible(dim: int, n:int, blocks: list[int], poss_set, prevs):
    """ niezmienniki
    -prevs to prefix tablicy, który mieści poprzednie bloki i kończy się pustym
    """
    k = len(blocks)
    if k == 0:
        prevs = prevs[:-1]
        l = len(prevs)
        prevs = prevs + (0,)*(dim-l)
        poss_set.add(prevs)
    else:
        left = 0
        right = n - (sum(blocks) + k - 1)
        for i in range(left, right+1):
            new_block = (0,)*i + (1,)*blocks[0] + (0,)
            new_n = n - (i+blocks[0]+1)
            new_blocks = blocks[1:]
            new_prevs = prevs+new_block
            iter_possible(dim, new_n, new_blocks, poss_set, new_prevs)

def consider(array: tuple, p: tuple, array_len: int):
    for i in range(array_len):
        if array[i] == 1 and p[i] == 0:
            return False
        elif array[i] == -1 and p[i] == 1:
            return False
    return True

def all_ones(idx, possibles):
    for p in possibles:
        if p[idx] == 0:
            return False
    return True

def all_zeros(idx, possibles):
    for p in possibles:
        if p[idx] == 1:
            return False
    return True

def iter_consider(array: list, possibles: set[tuple], array_len: int) -> tuple:
    """Iterate over possible values of array and delete impossible values.
    Then for every cell in row iterate over possible values and check whether
    0 or 1 can be set for sure. Return new_array with updated knowledge"""

    new_array = [0]* array_len
    for i in range(array_len):
        cnt = 0
        sum = 0
        base = array[i]
        for p in possibles:
            test = base + 2*p[i]
            if test == 1:
                possibles = possibles - {p}
            else:
                cnt += 1
                sum += p[i] 

        if sum == 0:
            new_array[i] = -1
        elif sum == cnt:
            new_array[i] = 1

    return tuple(new_array), possibles


def update_work_board(idx: int, max_row: int, new_array: tuple, board):
    if idx < max_row:
        row_idx = idx
        board[row_idx] = list(new_array)
    else:
        col_idx = idx - max_row
        for i in range(no_rows):
            board[i][col_idx] = new_array[i]
    return board

def infering_with_bt(work_board: list[list[int]], domains: dict):

    q = Queue()
    for w in range(R):
        if w < no_rows:
            row_idx = w
            q.put((w, domains[w]))
        else:
            col_idx = w - no_rows
            q.put((w, domains[w]))

    while q.qsize() > 0:
        w, possibles = q.get(0)
        no_before = len(possibles)

        if w < no_rows:
            row_idx = w
            prev_row = work_board[row_idx]
            new_row, new_possibles = iter_consider(prev_row, possibles, no_cols)
            work_board = update_work_board(w, no_rows, new_row, work_board)
            domains[w] = new_possibles
            if new_possibles == set():
                return False, work_board

            for i in range(no_cols):
                if prev_row[i] != new_row[i]:
                    q.put((no_rows + i, domains[no_rows + i]))

        else:
            col_idx = w - no_rows
            prev_col = [0]*no_rows
            for i in range(no_rows):
                prev_col[i] = work_board[i][col_idx]
            new_col, new_possibles = iter_consider(prev_col, possibles, no_rows)
            work_board = update_work_board(w, no_rows, new_col, work_board)
            domains[w] = new_possibles
            if new_possibles == set():
                return False, work_board

            for i in range(no_rows):
                if prev_col[i] != new_col[i]:
                    q.put((i, domains[i]))

        # write_solution_to_output(work_board)

    flag_return = True
    for i in range(no_rows):
        for j in range(no_cols):
            if work_board[i][j] == 0:
                flag_return = False
    if flag_return == True:
        return True, work_board

    # print("Made assumption")

    changed = False
    rand_pxl = 0
    while changed == False:
        # print("looking for unfinished cell")
        rand_row = rand_pxl // no_cols
        rand_col = rand_pxl % no_cols
        if work_board[rand_row][rand_col] == 0:
            changed = True
            break
        rand_pxl += 1
    
    rec_work_board = deepcopy(work_board)
    rec_domains = {}
    for k in domains.keys():
        rec_domains[k] = domains[k]

    rec_work_board[rand_row][rand_col] = -1
    # print("Made assumption " + str(rand_row) + ", " + str(rand_col))
    recursive_result, rec_work_board = infering_with_bt(rec_work_board, rec_domains) 
    if recursive_result == False:
        # print("Error!")
        for i in range(no_rows):
            for j in range(no_cols):
                rec_work_board[i][j] = work_board[i][j]
        for k in domains.keys():
            rec_domains[k] = domains[k]

        rec_work_board[rand_row][rand_col] = 1
        recursive_result, rec_work_board = infering_with_bt(rec_work_board, rec_domains) 
        return recursive_result, rec_work_board
    else:
        return True, rec_work_board

# work_board[1][1] = 1
# work_board[19][1] = 1
# work_board[8][8] = 1
# work_board[8][9] = 1

domains = {}
for w in range(R):
    if w < no_rows:
        row_idx = w
        possibles = generate_possible(no_cols, x_arr[row_idx])
        domains[w] = possibles
    else:
        col_idx = w - no_rows
        possibles = generate_possible(no_rows, y_arr[col_idx])
        domains[w] = possibles

result, work_board = infering_with_bt(work_board, domains)
if result == False:
    print("There is no solution!")
write_solution_to_output(work_board)