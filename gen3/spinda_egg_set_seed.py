# Script to find egg seeds for custom spinda on a set seed

from rngs import LCRNG

initial_advances = int(input("Initial Advances: "))
max_advances = int(input("Max Advances: "))
target_pid = int(input("Target PID: 0x"), 16)
seed = int(input("Initial Seed: 0x"), 16)

rng = LCRNG.PokeRNG(seed)
pid_low_found = False
pid_high_found = False
target_pid_low = (target_pid & 0xFFFF)-1
target_pid_high = target_pid >> 16
if target_pid_low == -1:
    print("PID not possible by egg")
    exit(0)

rng.advance(initial_advances)
for cnt in range(max_advances):
    go = LCRNG.PokeRNG(rng.seed)
    low = go.nextHigh()
    high = go.nextHigh()
    if (not pid_high_found) and low == target_pid_high:
        pid_high_found = True
        pid_high_advance = cnt
    if (not pid_low_found) and high == target_pid_low:
        pid_low_found = True
        pid_low_advance = cnt
    if pid_low_found & pid_high_found:
        print("Held Advance:",pid_low_advance+initial_advances,"Pickup Advance:",pid_high_advance+initial_advances)
        break
    rng.next()