# Dawid Sroka, zad1 z pracowni 3
#

from random import sample, randrange
from functools import cache
from queue import PriorityQueue, Queue

input_file = open("zad_input.txt", 'r')
output_file = open("zad_output.txt", 'w')
input_lines = input_file.readlines()

# Parse the input
x_dim, y_dim = [int(d) for d in input_lines[0].split()]
R = x_dim + y_dim
work_board = [[0 for x in range(y_dim)] for y in range(x_dim)]
board = [[0 for x in range(y_dim)] for y in range(x_dim)]
x_arr = [[int(d) for d in l.split()] for l in input_lines[1:x_dim+1]]
x_sum = [[0, sum(blocks)] for blocks in x_arr]
y_arr = [[int(d) for d in l.split()] for l in input_lines[x_dim+1:]]
y_sum = [[0, sum(blocks)] for blocks in y_arr]

def dump(m):
    for i in range(x_dim):
        line = ""
        for j in range(y_dim):
            if m[i][j] == 1:
                line += "#"
            elif m[i][j] == -1:
                line += " "
            else:
                line += "?"
        print(line)

def write_solution_to_output(m):
    for i in range(x_dim):
        line = ""
        for j in range(y_dim):
            if m[i][j] == 1:
                line += "#"
            else:
                line += "."
        output_file.write(line+"\n")

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
    k = len(blocks)
    if k == 0:
        prevs = prevs[:-1]
        l = len(prevs)
        prevs = prevs + (0,)*(dim-l)
        poss_set.add(prevs)
    else:
        for j in range(k):
            j += 1  # index from 1
            left = sum(blocks[:j-1]) + j-1
            right = n - (sum(blocks[j-1:]) + k - j)
            for i in range(left, right+1):
                new_block = (0,)*i + (1,)*blocks[j-1] + (0,)
                iter_possible(dim, n - (i+blocks[j-1]+1), blocks[1:], poss_set, prevs+new_block)

def rec_opt_dist(input_sequence: list[int], blocks: list[int]):
    return rec_opt_dist_inner(tuple(input_sequence), tuple(blocks))

@cache
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

def iter_consider(idx: int, array: tuple, possibles: set[tuple]):
    for p in possibles:
        if consider(array, p) == False:
            possibles = possibles - {p}
    return possibles



def main(work_board: list[list[int]]):
    for i in range(x_dim):
        added = overlapping_infer(work_board[i], x_arr[i])
        x_sum[i][0] += added

    for j in range(y_dim):
        col = [work_board[r][j] for r in range(x_dim)]
        added = overlapping_infer(col, y_arr[j])
        borders_infer(col,y_arr[j])

        for r in range(x_dim):
            work_board[r][j] = col[r]
    for i in range(x_dim):
        borders_infer(work_board[i], x_arr[i])

    pq = PriorityQueue()
    for w in range(R):
        if w < x_dim:
            row = w
            possibles = generate_possible(x_dim, x_arr[w])
            pq.put((-len(possibles),w, possibles))
        
    while pq.qsize() > 0:
        print("qsize = " + str(pq.qsize()))
        priority, w, possibles = pq.get(0)
        if w < x_dim:
            row = w
            print("w = " + str(w))
            if rec_opt_dist([max(0, i) for i in work_board[row]], x_arr[row]) != 0 :
                possibles = iter_consider(w, tuple(work_board[row]), possibles)
                print(len(possibles))
                pq.put((-len(possibles),row, possibles))


    
possibles = generate_possible(8, [1,4])
for i in range(len(possibles)):
    print(list(possibles)[i])
possibles = iter_consider(0, tuple([0,1,0,0,0,0,0,0]), possibles)
print("")
for i in range(len(possibles)):
    print(list(possibles)[i])


dist = rec_opt_dist([1,0,1,1,1,0,0,0], [1,4])
print(dist)


main(work_board)
dump(work_board)
