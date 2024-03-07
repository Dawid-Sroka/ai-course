def get_nth_line(file, n):
    for i, line in enumerate(file):
        if i == n:
            print(line)
            return line
        elif i > n:
            break

from bisect import bisect_left

with open("zad4_output.txt", 'r') as dict_file:
    lines = dict_file.readlines()
    print(lines[1])

f = open("words_for_ai1.txt")
lines = f.readlines()
print(lines[1])
print(lines[2000] > 'voiihkxrs')