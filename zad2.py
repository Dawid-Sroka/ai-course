zad = "zad2"

input_file = open(zad + "_input.txt", 'r')
output_file = open(zad + "_output.txt", 'w')
input_lines = input_file.readlines()


def print_split(word, word_len, prev):
    split = []
    prev_len = len(prev)
    # for i in range(word_len, 0,-1):
    i = word_len
    while i > 0:
        split.insert(0,word[prev[i]:i])
        i = prev[i]

    # for i in range(word_len, 0,-1):
    #     split.insert(0,word[prev[i]:i])
    # print(split)
    splitted = " ".join(split) + '\n'
    # print(splitted)
    output_file.write(splitted)

def opt_split(word, dict):
    word_len = len(word)
    dp = [0] * (word_len+1)
    prev = [0] * (word_len+1)
    for i in range(1,word_len+1):   # i is through dp
        # print(dp)
        max_dp = 0
        for j in range(i):          # j is through word
            candidate = word[j:i]
            if candidate+'\n' in dict:
                # print(candidate)
                candidate_max = dp[j] + len(candidate)**2
                if candidate_max > max_dp:
                    max_dp = candidate_max
                    prev[i] = j
        dp[i] = max_dp
    # print(dp[word_len])
    print_split(word, word_len, prev)

with open("words_for_ai1.txt", 'r') as dict_file:
    words = dict_file.readlines()
    # print(words[0:4])
    dict = set(words)
    for line in input_lines:
        opt_split(line.rstrip('\n'), dict)
    # opt_split('warasowa', dict)
