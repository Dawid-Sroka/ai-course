# Dawid Sroka, zad1 z pracowni 2
#
  

def convert_input_sequence(s: str) -> list:
    return [int(c) for c in s]

input_file = open("zad1_input.txt", 'r')
output_file = open("zad1_output.txt", 'w')
input_lines = input_file.readlines()

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


for line in input_lines:
    args = line.split()
    input_sequence = convert_input_sequence(args[0])
    D = [int(d) for d in args[1:]]
    # D = int(args[1])
    
    opt_cost = rec_opt_dist(input_sequence, D)
    print(opt_cost)
    output_file.write(str(opt_cost) + '\n')

    # opt_dist(input_sequence, D)
    