# Dawid Sroka, zad3 z pracowni 1
#

zad = "zad5"

input_file = open(zad + "_input.txt", 'r')
output_file = open(zad + "_output.txt", 'w')
input_lines = input_file.readlines()


x_dim, y_dim = [int(d) for d in input_lines[0].split()]
x_arr = [int(n) for n in input_lines[1:x_dim+1]]
y_arr = [int(n) for n in input_lines[x_dim+1:]]
print(x_dim)
print(y_dim)

