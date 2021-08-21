from MT import MT

target = 0x12345678

for seed in range(0x0,0x100000000):
    if MT(seed).next() == target:
        print(f"{seed:08X}")