# Dawid Sroka, zad3 z pracowni 1
#

from random import sample, randrange

zad = "zad"

input_file = open(zad + "_input.txt", 'r')
output_file = open(zad + "_output.txt", 'w')
input_lines = input_file.readlines()


x_dim, y_dim = [int(d) for d in input_lines[0].split()]
R = x_dim + y_dim
m = [[0 for x in range(y_dim)] for y in range(x_dim)]
# x_arr = [int(n) for n in input_lines[1:x_dim+1]]
# print(input_lines[1:x_dim+1])
x_arr = [[int(d) for d in l.split()] for l in input_lines[1:x_dim+1]]
# print(x_arr)
# y_arr = [int(n) for n in input_lines[x_dim+1:]]
y_arr = [[int(d) for d in l.split()] for l in input_lines[x_dim+1:]]
# print(y_arr)

def rec_opt_dist(input_sequence: list[int], blocks: list[int]):
    seq_len = len(input_sequence)
    k = len(blocks)
    if k == 0:
        return sum(input_sequence)
    right_bound = sum(blocks[1:]) + k-1

    frame = blocks[0]
    agg_seq = [0] * (seq_len + 1)
    for i in range(1,seq_len + 1):
        agg_seq[i] = agg_seq[i-1] + input_sequence[i-1]


    # aux_prefix = [0] * frame
    # working_seq = aux_prefix + input_sequence

    # prev_in_frame = 0
    max_in_frame = 0

    opt_cost = seq_len

    # for i in range(frame, seq_len - right_bound + frame):
    for i in range(frame, seq_len + 1 - right_bound):
        # in_frame = prev_in_frame + working_seq[i] - working_seq[i-frame]
        in_frame = agg_seq[i] - agg_seq[i-frame]
        rec_opt = rec_opt_dist(input_sequence[i+1:], blocks[1:])
        if in_frame > max_in_frame:
            max_in_frame = in_frame
        # prev_in_frame = in_frame

        # count_ones = sum(working_seq[:i+1])
        if i+1 == seq_len + 1:
            count_ones = agg_seq[i]
        else:
            count_ones = agg_seq[i+1]
        bits_to_unset = count_ones - in_frame
        bits_to_set = frame - in_frame
        cost = bits_to_unset + bits_to_set + rec_opt
        # answer = bits_to_unset + bits_to_set
        if cost < opt_cost:
            opt_cost = cost

    return opt_cost
    # output_file.write(str(answer) + '\n')

def dump(m):
    for i in range(x_dim):
        line = ""
        for j in range(y_dim):
            if m[i][j] == 1:
                line += "#"
            else:
                line += "."
        output_file.write(line+"\n")

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
    if rec_opt_dist(m[row], x_arr[row]) == 0:
        return True
    else:
        return False

def done_col(col):
    result = []
    for i in range(x_dim):
        result.append(m[i][col])
    if rec_opt_dist(result, y_arr[col]) == 0:
        return True
    else:
        return False
    
unfinished = set(range(R))

def main(unfinished):
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
            if r < 10:
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
            if r < 10:
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

main(unfinished)
dump(m)



# Dawid Sroka, zad1 z pracowni 2
#
  

# def convert_input_sequence(s: str) -> list:
#     return [int(c) for c in s]

# input_file = open("zad1_input.txt", 'r')
# output_file = open("zad1_output.txt", 'w')
# input_lines = input_file.readlines()




def opt_dist(input_sequence: list[int], D: int) -> None:
    seq_len = len(input_sequence)
    aux_prefix = [0] * D
    working_seq = aux_prefix + input_sequence

    prev_agg = 0
    max_agg = 0

    for i in range(D, seq_len + D):
        new_agg = prev_agg + working_seq[i] - working_seq[i-D]
        if(new_agg > max_agg):
            max_agg = new_agg
        prev_agg = new_agg

    count_ones = sum(working_seq)
    bits_to_unset = count_ones - max_agg
    bits_to_set = D - max_agg
    answer = bits_to_unset + bits_to_set
    
    output_file.write(str(answer) + '\n')


# for line in input_lines:
#     args = line.split()
#     input_sequence = convert_input_sequence(args[0])
#     D = [int(d) for d in args[1:]]
#     # D = int(args[1])
    
#     opt_cost = rec_opt_dist(input_sequence, D)
#     print(opt_cost)
#     output_file.write(str(opt_cost) + '\n')

#     # opt_dist(input_sequence, D)
