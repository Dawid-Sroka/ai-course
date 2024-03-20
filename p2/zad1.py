# Dawid Sroka, zad1 z pracowni 2
#
  

def convert_input_sequence(s: str) -> list:
    return [int(c) for c in s]

input_file = open("zad4_input.txt", 'r')
output_file = open("zad4_output.txt", 'w')
input_lines = input_file.readlines()

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
    
    output_file.write(str(answer) + '\n')


for line in input_lines:
    args = line.split()
    input_sequence = convert_input_sequence(args[0])
    D = int(args[1])
    
    opt_dist(input_sequence, D)