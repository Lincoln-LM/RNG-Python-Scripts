from MT import MT

rng = MT(int(input("Initial Seed: 0x"),16))
initial_advances = int(input("Initial Advances: "))
max_advances = int(input("Max Advances: "))
rng.advance(initial_advances)

print("----------------")

for cnt in range(max_advances):
    val = rng.nextUShort() & 0x3FFF
    if val == 0:
        print(f"{initial_advances+cnt} Pokerus found")
