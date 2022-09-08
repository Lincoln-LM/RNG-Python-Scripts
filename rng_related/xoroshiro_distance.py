"""
Efficiently calculate the distance between two Xoroshiro128+ states
"""
from xoroshiro_jump import compute_jump_polynomial, advance_via_jump
from rngs import Xoroshiro
from math import ceil, sqrt

def distance(start_rng: Xoroshiro.Xoroshiro, end_rng: Xoroshiro.Xoroshiro, max_advance):
    """Calculate the distance between start_rng and end_rng in O(sqrt(max_advance)) via BSGS"""
    lookup_table = []
    step_size = ceil(sqrt(max_advance))
    # TODO: actually jump backwards instead of period - jump_count
    backward_jump = compute_jump_polynomial(0x10008828e513b43d5095b8f76579aa001, (2 ** 128 - 1) - step_size)
    for _ in range(step_size):
        lookup_table.append(start_rng.state())
        start_rng.next()
    for i in range(step_size):
        try:
            j = lookup_table.index(end_rng.state())
            return i * step_size + j
        except ValueError:
            # state not found
            pass
        advance_via_jump(end_rng, backward_jump)
    return None

if __name__ == "__main__":
    start_rng = Xoroshiro.Xoroshiro(0x1234BEEFDEAD8765, 0x5678DEAD4321BEEF)
    end_rng = Xoroshiro.Xoroshiro(*start_rng.seed.copy())
    advance_via_jump(end_rng, compute_jump_polynomial(0x10008828e513b43d5095b8f76579aa001, 2 ** 24))
    print(distance(start_rng, end_rng, 2**32))
