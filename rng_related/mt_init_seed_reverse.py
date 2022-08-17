"""
Reverse the initial seed of a MT state
"""
from rngs import MT
# Script to get initial seed of a Mersenne Twister given the full untempered state
# Adapted from https://github.com/ambionics/mt_rand-reverse/blob/master/reverse_mt_rand.py

# Some terms:
# initial state = the mersenne twisters state before it is shuffled for the first time
# untempered state = the state before the temper function is applied (called when returning output to the user)
# tempered state = the state after tempering, this is what a 32 bit output would return

# Constants for our Mersenne Twister
STATE_MULT = 0x6C078965
STATE_MULT_INV = 0x9638806D
MAX = 0xffffffff
N = 624
M = 397

# Bitwise Operations
def lobits(v, b):
    return v & ((1 << b) - 1)
def bit(v, b):
    return v & (1 << b)
def bits(v, start, size):
    return lobits(v >> start, size)
def bv(v, b):
    return bit(v, b) >> b

# Reverse the function used to get the initial state from an initial seed
def reverse_init(s, i):
    s = (STATE_MULT_INV * (s - i)) & MAX
    return s ^ s >> 30

# Loop to do the above until you get to the initial seed
def reverse_state_init(s, p):
    for i in range(p, 0, -1):
        s = reverse_init(s, i)
    return s

# MTs shuffling function
def shuffle_single(m, u, v):
    mask = 0x9908b0df if v & 1 else 0
    return m ^ (((u & 0x80000000) | (v & 0x7FFFFFFF)) >> 1) ^ mask

# Loop through to do the above across the whole array
def shuffle(state):
    s = state
    for i in range(0, N - M):
        s[i] = shuffle_single(s[i+M], s[i], s[i+1])
    for i in range(N - M, N - 1):
        s[i] = shuffle_single(s[i+M-N], s[i], s[i+1])

# Undo the shuffling of the array given two untempered values 227 advances apart
# Can probably be simplified as we have the whole untempered array
def undo_shuffle(S000, S227):
    # S000 = rng.state[0]
    # S227 = rng.state[227]
    X = S000 ^ S227

    # check for mask, (LSB == 1)
    s22X_0 = bv(X, 31)
    # remove mask if present
    if s22X_0:
        X ^= 0x9908b0df

    # check for bit
    s227_31 = bv(X, 30)
    # remove bit if present
    if s227_31:
        X ^= 1 << 30

    # a bit of bruteforcing to find missing bits
    s228_1_30 = (X << 1)
    for s228_0 in range(2):
        for s228_31 in range(2):
            s228 = s228_0 | s228_31 << 31 | s228_1_30

            # check if the results line up with what we know
            s227 = reverse_init(s228, 228)
            if bv(s227, 0) != s22X_0:
                continue
            if bv(s227, 31) != s227_31:
                continue

            # check if the first result in the new state is the same as S000
            rand = reverse_state_init(s228, 228)
            rng = MT.MT(rand)
            rng.next()

            if not S000 == rng.state[0]:
                continue

            # found the initial seed
            return rand
    # no initial seed found
    return None

if __name__ == "__main__":
    rng = MT.MT(0x12345678)
    rng.next()
    print(hex(undo_shuffle(rng.state[0],rng.state[227])))
