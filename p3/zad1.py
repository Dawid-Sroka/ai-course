# Dawid Sroka, zad1 z pracowni 3
#

from random import sample, randrange
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

def dump(m):
    for i in range(x_dim):
        line = ""
        for j in range(y_dim):
            if m[i][j] == 1:
                line += "#"
            elif m[i][j] == -1:
                line += "."
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
    for j in range(k):
        j += 1  # index from 1
        left = sum(blocks[:j]) + j-1
        right = len(input_sequence) - (sum(blocks[j-1:]) + k - j)
        for i in range(right, left):
            input_sequence[i] = 1

def borders_infer(input_sequence: list[int], blocks: list[int]):
    dim = len(input_sequence)
    k = len(blocks)
    if input_sequence[0] == 1:
        for i in range(blocks[0]):
            input_sequence[i] = 1
        if blocks[0] < dim:
            input_sequence[blocks[0]] = -1
    if input_sequence[dim-1] == 1:
        for i in range(dim - blocks[k-1],dim):
            input_sequence[i] = 1
        if blocks[k-1] < dim:
            input_sequence[dim - blocks[k-1] - 1] = -1


def main(m: list[list[int]]):
    for i in range(x_dim):
        overlapping_infer(m[i], x_arr[i])

    for j in range(y_dim):
        col = [m[r][j] for r in range(x_dim)]
        overlapping_infer(col, y_arr[j])
        borders_infer(col,y_arr[j])

        for r in range(x_dim):
            m[r][j] = col[r]
    for i in range(x_dim):
        borders_infer(m[i], x_arr[i])

main(m)
dump(m)
write_solution_to_output(m)


# Functions for flipping specified bit in matrix
# def flip(matrix, row, col):
#     matrix[row][col] = 1 - matrix[row][col]

# def flip_in_row(matrix, row, col):
#     result = matrix[row].copy()
#     result[col] = 1 - result[col]
#     return result

# def flip_in_col(matrix, row, col):
#     result = [0] * x_dim
#     for i in range(x_dim):
#         result[i] = m[i][col]
#     result[row] = 1 - result[row]
#     return result

# # Functions for checking whether row/column satisfies specification
# def done_row(row):
#     if rec_opt_dist(m[row], x_arr[row]) == 0:
#         return True
#     else:
#         return False

# def done_col(col):
#     result = [0] * x_dim
#     for i in range(x_dim):
#         result[i] = m[i][col]
#     if rec_opt_dist(result, y_arr[col]) == 0:
#         return True
#     else:
#         return False


# # Main routine
# unfinished = set(range(R))


