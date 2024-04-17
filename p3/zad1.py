# Dawid Sroka, zad1 z pracowni 3
#

from random import sample, randrange
from functools import cache
from queue import Queue
from time import sleep

input_file = open("zad_input.txt", 'r')
output_file = open("zad_output.txt", 'w')
input_lines = input_file.readlines()

# Parse the input
no_rows, no_cols = [int(d) for d in input_lines[0].split()]
R = no_rows + no_cols
work_board = [[0 for x in range(no_cols)] for y in range(no_rows)]
board = [[0 for x in range(no_cols)] for y in range(no_rows)]
x_arr = [[int(d) for d in l.split()] for l in input_lines[1:no_rows+1]]
x_sum = [[0, sum(blocks)] for blocks in x_arr]
y_arr = [[int(d) for d in l.split()] for l in input_lines[no_rows+1:]]
y_sum = [[0, sum(blocks)] for blocks in y_arr]

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
    for i in range(no_rows):
        line = ""
        for j in range(no_cols):
            if m[i][j] == 1:
                line += "#"
            else:
                line += "."
        output_file.write(line+"\n")

# ===============================================        

def overlapping_infer(input_sequence: list[int], blocks: list[int]):
    k = len(blocks)
    added = 0
    for j in range(k):
        j += 1  # index from 1
        left = sum(blocks[:j]) + j-1
        right = len(input_sequence) - (sum(blocks[j-1:]) + k - j)
        for i in range(right, left):
            input_sequence[i] = 1
            added += 1
    return added


def borders_infer(input_sequence: list[int], blocks: list[int]):
    dim = len(input_sequence)
    k = len(blocks)
    added = 0
    if input_sequence[0] == 1:
        for i in range(blocks[0]):
            input_sequence[i] = 1
            added += 1
        if blocks[0] < dim:
            input_sequence[blocks[0]] = -1
    if input_sequence[dim-1] == 1:
        for i in range(dim - blocks[k-1],dim):
            input_sequence[i] = 1
            added += 1
        if blocks[k-1] < dim:
            input_sequence[dim - blocks[k-1] - 1] = -1
    return added


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


def iter_consider(array: tuple, possibles: set[tuple]) -> tuple:
    """Iterate over possible values of array and delete impossible values.
    Then for every cell in row iterate over possible values and check whether
    0 or 1 can be set for sure. Return new_array with updated knowledge"""
    for p in possibles:
        if consider(array, p) == False:
            possibles = possibles - {p}
    new_array = [0]* len(array)
    for i in range(len(array)):
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

def main(work_board: list[list[int]]):
    # dump(work_board)
    for i in range(no_rows):
        added = overlapping_infer(work_board[i], x_arr[i])
        x_sum[i][0] += added

    for j in range(no_cols):
        col_idx = [work_board[r][j] for r in range(no_rows)]
        added = overlapping_infer(col_idx, y_arr[j])
        borders_infer(col_idx,y_arr[j])

        for r in range(no_rows):
            work_board[r][j] = col_idx[r]
    for i in range(no_rows):
        borders_infer(work_board[i], x_arr[i])

    # sleep(1)
    # dump(work_board)

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
    
    while q.qsize() > 0:
        w, possibles = q.get(0)
        # dump(work_board)

        if w < no_rows:
            row_idx = w
            new_row, possibles = iter_consider(tuple(work_board[row_idx]), possibles)
            work_board = update_work_board(w, no_rows, new_row, work_board)

            row_array = [max(0, i) for i in work_board[row_idx]]
            if rec_opt_dist(row_array, x_arr[row_idx]) != 0 :
                q.put((w, possibles))

        else:
            col_idx = w - no_rows
            prev_col = [0]*no_rows
            for i in range(no_rows):
                prev_col[i] = work_board[i][col_idx]
            new_col, possibles = iter_consider(tuple(prev_col), possibles)
            work_board = update_work_board(w, no_rows, new_col, work_board)

            col_array = [max(0, i) for i in new_col]
            if rec_opt_dist(col_array, y_arr[col_idx]) != 0 :
                q.put((w, possibles))

        # dump(work_board)
        # sleep(0.1)

main(work_board)
write_solution_to_output(work_board)
