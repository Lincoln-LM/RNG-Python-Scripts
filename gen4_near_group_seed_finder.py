# Script to find the seed you hit based on your group seed

from MT import MT

target_seed = int(input("Target Seed: 0x"),16)
plus_minus = int(input("+/-: "))
advances_checked = int(input("Advances to check: "))
group_seed = int(input("Group Seed: 0x"),16)
for seed in range(target_seed-plus_minus,target_seed+plus_minus+1):
    go = MT(seed)
    for advance in range(advances_checked):
        if go.next() == group_seed:
            print(f"Initial Seed: {seed:08X}, Advance {advance}")