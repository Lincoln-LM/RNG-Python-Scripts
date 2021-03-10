import MT
import RNGPool

seed = int(input("Initial Seed: 0x"),16)
starting_frame = int(input("Starting Frame: "))
total_frames = int(input("Total Frames: "))

mt = MT.MT(seed)
mt.advance(starting_frame+1)
rngList = RNGPool.RNGList(mt,128)

for frame in range(total_frames):
    rngList.advanceFrames(60)
    EC = rngList.getValue()
    PID = rngList.getValue()
    IVs = [0]*6
    for c in range(6):
        if IVs[c] == 0:
            IVs[c] = rngList.getValue() >> 27
    print(frame+starting_frame,hex(PID), hex(EC), *IVs, sep=", ")
    rngList.advanceState()