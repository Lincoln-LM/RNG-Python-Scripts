"""
Hittable channel jirachi spread generator
"""

from rngs import LCRNG

natures = ['Hardy','Lonely','Brave','Adamant','Naughty','Bold','Docile','Relaxed','Impish','Lax','Timid','Hasty','Serious','Jolly','Naive','Modest','Mild','Quiet','Bashful','Rash','Calm','Gentle','Sassy','Careful','Quirky']

# Working backwards this validates if a Jirachi seed is obtainable
# There are 3 different patterns for this (6/7/8 advances) plus menu checking
def validate_jirachi(seed):
    rng = LCRNG.XDRNGR(seed)

    num1 = rng.nextHigh()
    num2 = rng.nextHigh()
    num3 = rng.nextHigh()

    rng.advance(3)
    if (num1 <= 0x4000): # 6 advances
        if (validate_menu(rng.seed)):
            return True

    rng.advance(1)
    if (num2 > 0x4000 and num1 <= 0x547a): # 7 advances
        if (validate_menu(rng.seed)):
            return True

    rng.advance(1)
    if (num3 > 0x4000 and num2 > 0x547a): # 8 advances
        if (validate_menu(rng.seed)):
            return True

    return False

# Working backwards from a seed check if the menu sequence will end on said seed
# Menu will advance the prng until it collects a 1, 2, and 3
def validate_menu(seed):
    mask = 0
    target = seed >> 30

    # Impossible to stop 0
    if (target == 0):
        return False
    else:
        mask |= 1 << target

    rng = LCRNG.XDRNGR(seed)
    while ((mask & 14) != 14):
        num = rng.next() >> 30

        # Basically this check means that while rolling for 1, 2, and 3
        # We hit our original target meaning that we can't land on the target
        if (num == target):
            return False

        mask |= 1 << num

    return True

seed = int(input("Seed: 0x"), 16)
start = int(input("Starting Advance: "))
advances = int(input("Advances: "))
rng = LCRNG.XDRNG(seed)
rng.advance(start)
print(f"{seed:X}")
print("Advance, Seed, Shiny, SID, PID, Nature, IVs")
for advance in range(advances):
    if validate_jirachi(rng.seed):
        filter = True
        go = LCRNG.XDRNG(rng.seed)

        tid = 40122
        sid = go.nextHigh()
        txor = tid^sid
        tsv = txor // 8
        high = go.nextHigh()
        low = go.nextHigh()
        
        # Skip Trainer info
        go.advance(3)

        if (0 if low > 7 else 1) != (high ^ 40122 ^ sid):
            high ^= 0x8000

        pxor = high ^ low
        psv = pxor // 8
        shiny = "No"
        if psv == tsv:
            shiny = "Star"
            if pxor == txor:
                shiny = "Square"
        # if shiny != "Star":
        #     filter = False
        #     rng.next()
        #     continue

        pid = (high << 16) | low
        nature = natures[pid%25]
        # if nature != "Jolly" and nature != "Careful" and nature != "Adamant":
        #     filter = False
        #     rng.next()
        #     continue
        ivs = [0]*6
        for i in range(6):
            if i == 3:
                i = 5
            elif i > 3:
                i -= 1
            ivs[i] = (go.nextHigh() >> 11)
        # if ivs[0] < 28 or ivs[1] < 28 or ivs[2] < 28 or ivs[4] < 28 or ivs[5] < 28:
        #     filter = False
        #     rng.next()
        #     continue

        if filter:
            print(f"{start+advance}, {rng.seed:08X}, {shiny}, {sid:05}, {pid:08X}, {nature}, {str(ivs)}")
    rng.next()
