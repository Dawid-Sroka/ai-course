zad = "zad2"

input_file = open(zad + "_input.txt", 'r')
output_file = open(zad + "_output.txt", 'w')
input_lines = input_file.readlines()


def print_split(word, word_len, prev):
    split = []
    i = word_len
    while i > 0:
        split.insert(0,word[prev[i]:i])
        i = prev[i]
    splitted = " ".join(split) + '\n'
    output_file.write(splitted)

def opt_split(word, dict):
    word_len = len(word)
    dp = [0] * (word_len+1)
    prev = [0] * (word_len+1)
    for i in range(1,word_len+1):   # i is through dp
        max_dp = 0
        for j in range(i):          # j is through word
            candidate = word[j:i] + '\n'
            if candidate in dict:
                candidate_max = dp[j] + (i-j)**2
                if candidate_max > max_dp:
                    max_dp = candidate_max
                    prev[i] = j
        dp[i] = max_dp
    print_split(word, word_len, prev)

with open("words_for_ai1.txt", 'r') as dict_file:
    words = dict_file.readlines()
    dict = set(words)
    for line in input_lines:
        opt_split(line.rstrip('\n'), dict)
