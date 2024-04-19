# Dawid Sroka, zad1 z pracowni 3
#

from random import sample, randrange
from functools import cache
from queue import Queue
from time import sleep
from copy import deepcopy

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



def rec_opt_dist(input_sequence: list[int], blocks: list[int]):
    return rec_opt_dist_inner(tuple(input_sequence), tuple(blocks))

# @cache
def rec_opt_dist_inner(input_sequence: tuple[int], blocks: tuple[int]):
    seq_len = len(input_sequence)
    k = len(blocks)
    if k == 0:
        return sum(input_sequence)
    right_bound = sum(blocks[1:]) + k-1

    frame = blocks[0]
    agg_seq = [0] * (seq_len + 1)
    for i in range(1,seq_len + 1):
        agg_seq[i] = agg_seq[i-1] + input_sequence[i-1]

    max_in_frame = 0
    opt_cost = seq_len

    for i in range(frame, seq_len + 1 - right_bound):
        in_frame = agg_seq[i] - agg_seq[i-frame]
        rec_opt = rec_opt_dist(input_sequence[i+1:], blocks[1:])
        if in_frame > max_in_frame:
            max_in_frame = in_frame

        if i+1 == seq_len + 1:
            count_ones = agg_seq[i]
        else:
            count_ones = agg_seq[i+1]

        bits_to_unset = count_ones - in_frame
        bits_to_set = frame - in_frame
        cost = bits_to_unset + bits_to_set + rec_opt
        if cost < opt_cost:
            opt_cost = cost

    return opt_cost

def consider(array: tuple, p: tuple):
    d = len(array)
    for i in range(d):
        if array[i] == 1 and p[i] == 0:
            return False
        elif array[i] == -1 and p[i] == 1:
            return False
    return True

def all_ones(idx, possibles):
    for p in possibles:
        if idx >= len(p) :
            print(idx)
            print(possibles)
            raise IndexError
        if p[idx] == 0:
            return False
    return True

def all_zeros(idx, possibles):
    for p in possibles:
        if p[idx] == 1:
            return False
    return True


def iter_consider(array: tuple, possibles: set[tuple], array_len: int) -> tuple:
    """Iterate over possible values of array and delete impossible values.
    Then for every cell in row iterate over possible values and check whether
    0 or 1 can be set for sure. Return new_array with updated knowledge"""
    for p in possibles:
        if consider(array, p) == False:
            possibles = possibles - {p}
    new_array = [0]* array_len
    for i in range(array_len):
        if all_ones(i, possibles):
            new_array[i] = 1
        if all_zeros(i, possibles):
            new_array[i] = -1
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


def infering_with_bt(work_board: list[list[int]]):

    q = Queue()
    for w in range(R):
        if w < no_rows:
            row_idx = w
            possibles = generate_possible(no_cols, x_arr[row_idx])
            q.put((w, possibles))
        else:
            col_idx = w - no_rows
            possibles = generate_possible(no_rows, y_arr[col_idx])
            q.put((w, possibles))

    board_flag = False
    cnt = 0
    while q.qsize() > 0:
        # print("get from queue")
        w, possibles = q.get(0)
        no_before = len(possibles)
        # dump(work_board)

        if w < no_rows:
            row_idx = w
            new_row, possibles = iter_consider(tuple(work_board[row_idx]), possibles, no_cols)
            work_board = update_work_board(w, no_rows, new_row, work_board)
            if possibles == set():
                # print("contradiction!")``
                return False, work_board
            no_current = len(possibles)

            row_array = [max(0, i) for i in work_board[row_idx]]
            # if rec_opt_dist(row_array, x_arr[row_idx]) != 0 :
            if sum(row_array) < sum(x_arr[row_idx]) :
                q.put((w, possibles))
            if no_current < no_before:
                # q.put((w, possibles))
                board_flag = True

        else:
            col_idx = w - no_rows
            prev_col = [0]*no_rows
            for i in range(no_rows):
                prev_col[i] = work_board[i][col_idx]
            new_col, possibles = iter_consider(tuple(prev_col), possibles, no_rows)
            work_board = update_work_board(w, no_rows, new_col, work_board)
            if possibles == set():
                return False, work_board
            no_current = len(possibles)

            col_array = [max(0, i) for i in new_col]
            # if rec_opt_dist(col_array, y_arr[col_idx]) != 0 :
            if sum(col_array) < sum(y_arr[col_idx]) :
                q.put((w, possibles))

            if no_current < no_before:
            #     q.put((w, possibles))
                board_flag = True


        # dump(work_board)
        # sleep(0.1)
        # write_solution_to_output(work_board)

        cnt += 1
        if cnt > R+2:
            cnt = 0
            if board_flag == False:
                break
            board_flag = False

    flag_return = True
    for i in range(no_rows):
        for j in range(no_cols):
            if work_board[i][j] == 0:
                flag_return = False
    if flag_return == True:
        return True, work_board

    # dump(work_board)
    # sleep(1)
    # print("Made assumption")

    changed = False
    while changed == False:
        # print("looking for unfinished cell")
        rand_pxl = int(randrange(no_cols * no_rows))
        rand_row = rand_pxl // no_cols
        rand_col = rand_pxl % no_cols
        if work_board[rand_row][rand_col] == 0:
            changed = True
    
    rec_work_board = deepcopy(work_board)
    rec_work_board[rand_row][rand_col] = 1
    # print("Made assumption " + str(rand_row) + ", " + str(rand_col))
    recursive_result, rec_work_board = infering_with_bt(rec_work_board) 
    if recursive_result == False:
        # print("Error!")
        rec_work_board2 = deepcopy(work_board)
        rec_work_board2[rand_row][rand_col] = -1
        recursive_result, rec_work_board2 = infering_with_bt(rec_work_board2) 
        # if recursive_result == False:
        return recursive_result, rec_work_board2
    else:
        return True, rec_work_board

    # return True

# work_board[1][1] = 1
# work_board[8][8] = 1
# work_board[8][9] = 1

result, work_board = infering_with_bt(work_board)
if result == False:
    print("There is no solution!")
write_solution_to_output(work_board)