import MT
import RNGPool

seed = int(input("Initial Seed: 0x"),16)
starting_frame = int(input("Starting Frame: "))
total_frames = int(input("Total Frames: "))

mt = MT.MT(seed)
rngList = RNGPool.RNGList(mt,128)
rngList.advanceStates(starting_frame+1)

def rand(n):
    return (rngList.getValue()*n>>32) & 0xFFFFFFFF

for frame in range(total_frames):
    rngList.advanceFrames(68)
    EC = rngList.getValue()
    PID = rngList.getValue()
    IVs = [0]*6
    i = 3
    while i > 0:
        tmp = rand(6)
        if IVs[tmp] == 0:
            i -= 1
            IVs[tmp] = 31
    for c in range(6):
        if IVs[c] == 0:
            IVs[c] = rngList.getValue() >> 27
    print(frame+starting_frame,hex(PID), hex(EC), *IVs, sep=", ")
    rngList.advanceState()