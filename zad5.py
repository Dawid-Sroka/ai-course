# Dawid Sroka, zad3 z pracowni 1
#

from random import uniform, sample, randrange
from math import floor

zad = "zad5"

input_file = open(zad + "_input.txt", 'r')
output_file = open(zad + "_output.txt", 'w')
input_lines = input_file.readlines()


x_dim, y_dim = [int(d) for d in input_lines[0].split()]
D = x_dim + y_dim
m = [[0 for x in range(y_dim)] for y in range(x_dim)]
x_arr = [int(n) for n in input_lines[1:x_dim+1]]
y_arr = [int(n) for n in input_lines[x_dim+1:]]
print(x_dim)
print(y_dim)


def opt_dist(input_sequence: list[int], D: int) -> None:
    seq_len = len(input_sequence)
    aux_prefix = [0] * D
    working_seq = aux_prefix + input_sequence

    agg_seq = [0] * (D + seq_len)
    max_agg = 0

    for i in range(D, seq_len + D):
        agg_seq[i] = agg_seq[i-1] + working_seq[i] - working_seq[i-D]
        if(agg_seq[i] > max_agg):
            max_agg = agg_seq[i]

    count_ones = sum(working_seq)
    bits_to_unset = count_ones - max_agg
    bits_to_set = D - max_agg
    answer = bits_to_unset + bits_to_set
    return answer

def dump(m):
    for i in range(x_dim):
        line = ""
        for j in range(y_dim):
            if m[i][j] == 1:
                line += "#"
            else:
                line += "."
        print(line)
        output_file.write(line+"\n")
        # print("".join(str(x) for x in m[i]))

def flip(matrix, row, col):
    if matrix[row][col] == 0:
        matrix[row][col] = 1
    else:
        matrix[row][col] = 0

def flip_in_row(matrix, row, col):
    result = matrix[row].copy()
    if matrix[row][col] == 0:
        result[col] = 1
    else:
        result[col] = 0
    return result

def flip_in_col(matrix, row, col):
    result = []
    for i in range(x_dim):
        result.append(m[i][col])
    if matrix[row][col] == 0:
        result[row] = 1
    else:
        result[row] = 0
    return result

def done_row(row):
    if opt_dist(m[row], x_arr[row]) == 0:
        return True
    else:
        return False

def done_col(col):
    result = []
    for i in range(x_dim):
        result.append(m[i][col])
    if opt_dist(result, y_arr[col]) == 0:
        return True
    else:
        return False
    
# unfinished = set(present)
unfinished = set(range(D))
print(unfinished)

def main(unfinished):
    while len(unfinished) > 0:
    # for i in range(30):
        victim = sample(sorted(unfinished),1)[0]
        # victim = randrange(0,x_dim)
        print(victim)
        if victim < x_dim:
            row = victim

            print("row")
            min_dist = x_dim + y_dim
            min_pos = 0
            for col in range(y_dim):
                flipped = flip_in_row(m, row, col)
                row_cost = opt_dist(flipped, x_arr[row])
                flipped = flip_in_col(m, row, col)
                col_cost = opt_dist(flipped, y_arr[col])
                if min_dist > row_cost + col_cost :
                    min_dist = row_cost + col_cost
                    min_pos = col
            print(min_dist)
            print(min_pos)

            r = randrange(100)
            if r < 10:
                min_pos = randrange(y_dim)

            flip(m,row,min_pos)
            print()
            # dump(m)
            if done_row(row):
                unfinished = unfinished - {victim}
            else:
                unfinished = unfinished | {victim}
            if done_col(min_pos):
                unfinished = unfinished - {min_pos + x_dim}
            else:
                unfinished = unfinished | {min_pos + x_dim}
        else:
            col = victim - x_dim
            print("col")
            min_dist = x_dim + y_dim
            min_pos = 0
            for row in range(x_dim):
                flipped = flip_in_row(m, row, col)
                row_cost = opt_dist(flipped, x_arr[row])
                flipped = flip_in_col(m, row, col)
                col_cost = opt_dist(flipped, y_arr[col])
                if min_dist > row_cost + col_cost :
                    min_dist = row_cost + col_cost
                    min_pos = row
            print(min_dist)
            print(min_pos)

            r = randrange(100)
            if r < 10:
                min_pos = randrange(x_dim)

            flip(m,min_pos,col)
            print()
            # dump(m)
            if done_col(col):
                unfinished = unfinished - {victim}
            else:
                unfinished = unfinished | {victim}
            if done_row(min_pos):
                unfinished = unfinished - {min_pos}
            else:
                unfinished = unfinished | {min_pos}

main(unfinished)
dump(m)
# f = flip_in_col(m,2,1)
# print(f)
