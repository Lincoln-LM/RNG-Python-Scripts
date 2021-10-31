from TinyMT import TinyMT
from random import randint

def reverse_tinymt(state):
    state_copy = state.copy()
    y_final = state_copy[3]
    
    if y_final & 1:
        state_copy[1] ^= 0x8f7011ee
        state_copy[2] ^= 0xfc78ff1f

    x_final = state_copy[2] ^ (y_final << 10)

    state_copy[2] = state_copy[1]
    state_copy[1] = state_copy[0]
    
    x_before = 0
    last_used_bit = 0
    for bit in range(0,32):
        last_used_bit = (x_final ^ (last_used_bit << 1)) & (1 << bit)
        x_before |= last_used_bit
    
    y_middle = y_final ^ x_final
    y_before = 0
    last_used_bit = 0
    for bit in range(31,-1,-1):
        last_used_bit = (y_middle ^ (last_used_bit >> 1)) & (1 << bit)
        y_before |= last_used_bit

    state_copy[0] = x_before ^ state_copy[1] ^ state_copy[2]
    state_copy[3] = y_before
    
    return state_copy

# rng = TinyMT(state=[283379028, 1408124395, 1944874483, 651100764])
rng = TinyMT(seed=0x87654432)
print(rng.state)
c = 0
b = 0
state = rng.state.copy()
while c < 9:
    if c < 6:
        # print(f"1/{3**(c)}")
        if (rng.next() * 3**(c)) >> 32 == 0:
            c += 1
        else:
            c = 0
            state = rng.state.copy()
    else:
        # print(f"1/{3**6}")
        if (rng.next() * 3**6) >> 32 == 0:
            c += 1
        else:
            c = 0
            state = rng.state.copy()
    if c > b:
        b = c
        print(b+1,[i for i in state])