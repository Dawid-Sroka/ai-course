# Dawid Sroka, zad1 z pracowni 3
#
# Powtarzam moje rozwiązanie z5/p1, ale tym razem funkcja opt_dist
# została zmodyfikowana do funkcji rec_opt_dist. Jest to prosta rekurencyjna
# implementacja.
# Jeśli w wierszu W mają być bloki d1, d2, ..., dk to biorę d1
# i rozpatruje każdą możliwę pozycję j bloku d1 w W (czyli albo maksymalnie na 
# lewo, albo tak daleko na prawo, żeby wciąż zmieściły się pozostałe bloki).
# Następnie rekurencyjnie wywołuję się na W[j:] oraz d2,..., dk.
# Rozpatrując wszystkie pozycje, znajduję minimalny koszt.
#
# Oprócz tego zawsze z prawdopodobieństwem r_prob dokonuję nieoptymalnej zmiany
# oraz zaczynam rozwiązywanie od nowa, jeśli minęł czas time_limit sekund

from random import sample, randrange
from time import time
from functools import cache

input_file = open("zad_input.txt", 'r')
output_file = open("zad_output.txt", 'w')
input_lines = input_file.readlines()

# Parse the input
x_dim, y_dim = [int(d) for d in input_lines[0].split()]
R = x_dim + y_dim
m = [[0 for x in range(y_dim)] for y in range(x_dim)]
x_arr = [[int(d) for d in l.split()] for l in input_lines[1:x_dim+1]]
y_arr = [[int(d) for d in l.split()] for l in input_lines[x_dim+1:]]

# Constants
r_prob = 15
time_limit = 8

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

def write_solution_to_output(m):
    for i in range(x_dim):
        line = ""
        for j in range(y_dim):
            if m[i][j] == 1:
                line += "#"
            else:
                line += "."
        output_file.write(line+"\n")

# Functions for flipping specified bit in matrix
def flip(matrix, row, col):
    if matrix[row][col] == 0:
        matrix[row][col] = 1
    else:
        matrix[row][col] = 0

def flip_in_row(matrix, row, col):
    result = matrix[row].copy()
    result[col] = 1 - result[col]
    return result

def flip_in_col(matrix, row, col):
    result = [0] * x_dim
    for i in range(x_dim):
        result[i] = m[i][col]
    result[row] = 1 - result[row]
    return result

# Functions for checking whether row/column satisfies specification
def done_row(row):
    if rec_opt_dist(m[row], x_arr[row]) == 0:
        return True
    else:
        return False

def done_col(col):
    result = [0] * x_dim
    for i in range(x_dim):
        result[i] = m[i][col]
    if rec_opt_dist(result, y_arr[col]) == 0:
        return True
    else:
        return False


# Main routine
unfinished = set(range(R))

def main(unfinished):
    start = time()
    while len(unfinished) > 0:
        victim = sample(sorted(unfinished),1)[0]
        if victim < x_dim:
            row = victim

            min_dist = x_dim + y_dim
            min_pos = 0
            for col in range(y_dim):
                flipped = flip_in_row(m, row, col)
                row_cost = rec_opt_dist(flipped, x_arr[row])
                flipped = flip_in_col(m, row, col)
                col_cost = rec_opt_dist(flipped, y_arr[col])
                if min_dist > row_cost + col_cost :
                    min_dist = row_cost + col_cost
                    min_pos = col

            r = randrange(100)
            if r < r_prob:
                min_pos = randrange(y_dim)

            flip(m,row,min_pos)
            if done_row(row):
                unfinished = unfinished - {victim}
            else:
                unfinished = unfinished | {victim}
            if done_col(min_pos):
                unfinished = unfinished - {min_pos + x_dim}
            else:
                unfinished = unfinished | {min_pos + x_dim}

            t = time()
            if t - start > time_limit:
                return False
        else:
            col = victim - x_dim
            min_dist = x_dim + y_dim
            min_pos = 0
            for row in range(x_dim):
                flipped = flip_in_row(m, row, col)
                row_cost = rec_opt_dist(flipped, x_arr[row])
                flipped = flip_in_col(m, row, col)
                col_cost = rec_opt_dist(flipped, y_arr[col])
                if min_dist > row_cost + col_cost :
                    min_dist = row_cost + col_cost
                    min_pos = row

            r = randrange(100)
            if r < r_prob:
                min_pos = randrange(x_dim)

            flip(m,min_pos,col)
            if done_col(col):
                unfinished = unfinished - {victim}
            else:
                unfinished = unfinished | {victim}
            if done_row(min_pos):
                unfinished = unfinished - {min_pos}
            else:
                unfinished = unfinished | {min_pos}
            t = time()
            if t - start > time_limit:
                return False

    write_solution_to_output(m)
    return True

# Execute main routine until it solves
while True:
    if main(unfinished) == True:
        break
