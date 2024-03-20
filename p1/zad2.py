# Dawid Sroka, zad2 z pracowni 1
#
# Programowanie dynamiczne, złożoność długość_tekstu**2
# dp[i] przechowuje zmaksymalizowaną wartość dla prefixu text[0:i]
# Aby obliczyć dp[i] musimy rozważyć wybranie każdego sufixu text[0:i]
# jako słowa w podziale. Robimy to w zagnieżdżonej pętli.

zad = "zad2"

input_file = open(zad + "_input.txt", 'r')
output_file = open(zad + "_output.txt", 'w')
input_lines = input_file.readlines()


def print_split(text, text_len, prev):
    split = []
    i = text_len
    while i > 0:
        split.insert(0,text[prev[i]:i])
        i = prev[i]
    splitted = " ".join(split) + '\n'
    output_file.write(splitted)

def opt_split(text, words_set):
    text_len = len(text)
    dp = [0] * (text_len+1)
    prev = [0] * (text_len+1)
    for i in range(1,text_len+1):   # i is through dp
        max_dp = 0
        for j in range(i):          # j is through text
            candidate = text[j:i] + '\n'
            if candidate in words_set:
                candidate_max = dp[j] + (i-j)**2
                if candidate_max > max_dp:
                    max_dp = candidate_max
                    prev[i] = j
        dp[i] = max_dp
    print_split(text, text_len, prev)

with open("words_for_ai1.txt", 'r') as dict_file:
    words = dict_file.readlines()
    S = set(words)
    for t in input_lines:
        t = t.rstrip('\n')
        opt_split(t, S)
