# script to reverse tinymt

from TinyMT import TinyMT
from random import randint, seed

def reverse_tinymt(state):
    state_copy = state.copy()
    # The final value of y is stored directly in index 3
    ## self.state[3] = y
    y_final = state_copy[3]
    
    # This undoes the following
    ## ^ ((y & 1) * 0x8f7011ee))
    ## ^ ((y & 1) * 0xfc78ff1f))
    # We can undo the XORs by simply doing them again
    if y_final & 1:
        state_copy[1] ^= 0x8f7011ee
        state_copy[2] ^= 0xfc78ff1f

    # Once we've reversed the above, we can calculate the final value of x by undoing another XOR
    ## x ^ (y << 10)
    x_final = state_copy[2] ^ (y_final << 10)

    ## self.state[0] = self.state[1]
    ## self.state[1] = (self.state[2]
    state_copy[2] = state_copy[1]
    state_copy[1] = state_copy[0]
    
    # This is used to undo the following
    ## x ^= (x << 1)
    ## y ^= ((y >> 1) ^ x)
    # Theres probably a better approach but this is what we're using
    
    # x_before  = ABCDEFGH
    # x_shifted = BCDEFGH0
    # x_final   = IJKLMNOP
    # P = H^0, H = P
    # O = G^H, G = O^H, G = O^P
    # N = F^G, F = N^G, F = N^O^P
    # pattern continues
    x_before = 0
    last_used_bit = 0
    for bit in range(0,32):
        last_used_bit = (x_final ^ (last_used_bit << 1)) & (1 << bit)
        x_before |= last_used_bit
    
    # y_middle  = ABCDEFGH
    # y_shifted = 0ABCDEFG
    # y_final   = IJKLMNOP
    # I = A^0, A = I
    # J = B^A, B = J^A, B = J^I
    # K = C^B, C = K^B, C = K^J^I
    # pattern continues
    y_middle = y_final ^ x_final
    y_before = 0
    last_used_bit = 0
    for bit in range(31,-1,-1):
        last_used_bit = (y_middle ^ (last_used_bit >> 1)) & (1 << bit)
        y_before |= last_used_bit

    # Now that we have x_before and y_before, we can calculate state[0] and state[3]
    # Undo some more XORs
    ## x = self.state[0] ^ self.state[1] ^ self.state[2]
    state_copy[0] = x_before ^ state_copy[1] ^ state_copy[2]
    # y_before is set directly to state[3]
    ## y = self.state[3]
    state_copy[3] = y_before
    
    # Return our fully calculated previous state
    return state_copy

# Create a TinyMT object with a random initial state
rng = TinyMT(state=[randint(1,0xFFFFFFFF) for i in range(4)])
# Chop off the unused bit for cleanliness
rng.state[0] &= 0x7FFFFFFF
# Print our initial state
print(f"Initial State: \t\t\t{[f'{i:08X}' for i in rng.state]}")
# Advance the rng once so we can test whether or not it works
rng.nextState()
# Print the state thats being fed to the function
print(f"Next State: \t\t\t{[f'{i:08X}' for i in rng.state]}")
# Calculate our initial state and print to compare
print(f"Predicted Initial State: \t{[f'{i:08X}' for i in reverse_tinymt(rng.state)]}")

# Test 10000 times
print("Testing 10000 times....")
for test in range(10000):
    rng = TinyMT(state=[randint(1,0xFFFFFFFF) for i in range(4)])
    rng.state[0] &= 0x7FFFFFFF
    initial_state = rng.state.copy()
    rng.nextState()
    if initial_state != reverse_tinymt(rng.state):
        print(f"Unsuccessfully predicted init:{initial_state} pred:{reverse_tinymt(rng.state)}")
        break
else:
    print("Successfully predicted 10000 tinymt advances")