from queue import Queue
from sys import argv

class State:
    def __init__(self, d: int, s: str):
        self.dist = d
        self.sequence = s
        self.visited = False

def flip_to_one():
    pass

def flip(state: State, idx: int):
    seq = state.sequence
    max_idx = len(seq)
    if (seq[idx] == '1'):
        flipped_bit = '0'
    else:
        flipped_bit = '1'
    return seq[0:idx] + flipped_bit + seq[idx+1:max_idx]


def check(state: State, D: int) -> bool:
    seq = state.sequence
    seq = seq.strip('0')
    if(len(seq) != D):
        return False
    for i in range(len(seq)):
        if (seq[i] == '0'):
            return False
    return True


input_sequence = argv[1]
D: int = int(argv[2])
seq_len = len(input_sequence)

state0 = State(0, input_sequence)
q = Queue()
q.put(state0)
answer = -1

while (q.qsize() > 0):
    s = q.get()
    print(s.sequence)
    s.visited = True
    if (check(s, D) == True):
        answer = s.dist
        break

    for i in range(seq_len):
        neigh = State(s.dist +1, flip(s, i))
        q.put(neigh)

print(answer)
