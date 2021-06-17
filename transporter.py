import MT
import RNGPool

seed = int(input("Initial Seed: 0x"),16)
starting_frame = int(input("Starting Frame: "))
total_frames = int(input("Total Frames: "))
delay = int(input("Delay: "))
typ = int(input("Pokemon Type (0 = Genderless 1 = Random Gender 2 = Mythical): "))
shiny_locked = int(input("Shiny Locked? (0 = Forced Shiny 1 = Shiny Locked): "))
TID = int(input("TID: "))
star_check = int(input("Search for Star frames only? (0 = No 1 = Yes): "))
print()

TXOR = (TID ^ 00000)
TSV = TXOR//16

advance_table = [4,5,2]
iv_table = [3,3,5]

mt = MT.MT(seed)
rngList = RNGPool.RNGList(mt,1024)
rngList.advanceStates(starting_frame+1+delay)

def rand(n):
    return (rngList.getValue() * n>>32) & 0xFFFFFFF
def rand2():
    return rngList.getValue() < 0x80000000

print("Frame, IVs, PSV, PID, EC, Shiny")
for frame in range(total_frames):
    EC = rngList.getValue()

    PID = rngList.getValue()
    PXOR = ((PID >> 16) ^ (PID & 0xFFFF))
    PSV = PXOR//16
    shiny = "No"
    if PSV == TSV:
        if shiny_locked:
            PID ^= 0x10000000
        else:
            if PXOR == TXOR:
                shiny = "Square"
            else:
                shiny = "Star"
    elif not shiny_locked:
        shiny = "Square"
        PID = (((TXOR ^ (PID & 0xFFFF)) << 16) | (PID & 0xFFFF)) & 0xFFFFFFFF
    PXOR = ((PID >> 16) ^ (PID & 0xFFFF))
    PSV = PXOR//16

    if star_check and shiny != "Star":
        rngList.advanceState()
        continue

    IVs = [-1]*6
    i = iv_table[typ]
    while i > 0:
        tmp = rand(6)
        if (IVs[tmp] < 0):
            i -= 1
            IVs[tmp] = 31
    for i in range(6):
        if IVs[i] < 0:
            IVs[i] = rngList.getValue() >> 27
    ivstring = str(IVs).replace('[','').replace(']','').replace(' ','')
    print(f"{frame+starting_frame}, {ivstring}, {PSV}, {PID:X}, {EC:X}, {shiny}")

    rngList.advanceState()
    
