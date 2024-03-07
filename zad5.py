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
arr = [int(n) for n in input_lines[1:]]
x_arr = [int(n) for n in input_lines[1:x_dim+1]]
y_arr = [int(n) for n in input_lines[x_dim+1:]]
print(x_dim)
print(y_dim)

x_present = [0] * x_dim
x_position = [-1] * x_dim
y_present = [0] * y_dim
y_position = [-1] * y_dim
present = [0] * D
position = [0] * D

# unfinished = set(present)
unfinished = set(range(D))
print(unfinished)

def can_add_in_col(row, col):
    if x_position[row] <= col < x_position[row] + x_present[row]:
        print("no")
        return False
    elif y_present[col] == y_arr[col]:
        return False
    elif row == y_position[col] - 1:
        return True
    elif row == y_position[col] + y_present[col]:
        return True
    elif y_present[col] == 0:
        return True
    else:
        return False

# assumes 
def gain_row(row, col):


while len(unfinished) > 0:
    victim = uniform(0,1)
    victim = sample(sorted(unfinished),1)
    print(victim)
    if victim[0] < x_dim:
        # row
        print("row")
        if x_present[row] == 0:
            can_add_in_col
        else:

        for col in range(y_dim):
            if col == x_position[row] - 1 :
            if can_add_in_col(victim, i):

        break
    else:
        victim = victim - x_dim
        pass


