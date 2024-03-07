# Dawid Sroka, zad3 z pracowni 1
#

from random import uniform, sample
from math import floor

zad = "zad5"

input_file = open(zad + "_input.txt", 'r')
output_file = open(zad + "_output.txt", 'w')
input_lines = input_file.readlines()


x_dim, y_dim = [int(d) for d in input_lines[0].split()]
D = x_dim + y_dim
r = x_dim / D
m = [[0 for x in range(y_dim)] for y in range(x_dim)]

arr = [int(n) for n in input_lines[1:]]
x_arr = [int(n) for n in input_lines[1:x_dim+1]]
y_arr = [int(n) for n in input_lines[x_dim+1:]]
print(x_dim)
print(y_dim)

x_cnt = [0] * x_dim
y_cnt = [0] * y_dim

present = [0] * D

# unfinished = set(present)
unfinished = set(range(D))
print(unfinished)

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

def flip(matrix, row, col):
    result = matrix
    if matrix[row][col] == 0:
        result[row][col] = 1
    else:
        result[row][col] = 0
    return result

def flip_in_row(matrix, row, col):
    result = matrix[row].copy()
    if matrix[row][col] == 0:
        result[col] = 1
    else:
        result[col] = 0
    return result
    
def main():
    # while len(unfinished) > 0:
    for i in range(1):
        # victim = uniform(0,1)
        victim = sample(sorted(unfinished),1)[0]
        print(victim)
        victim = 2
        if victim < x_dim:
            row = victim
            print("row")
            for col in range(y_dim):
                min_dist = x_dim
                flipped = flip_in_row(m, row, col)
                print(flipped)
                candidate = opt_dist(flipped, x_arr[row])
                print(candidate)
                min_dist = min(min_dist, candidate)
            print(min_dist)
        else:
            victim = victim - x_dim
            break

main()
