import MT
import RNGPool
import math

seed = int(input("Initial Seed: 0x"),16)
starting_frame = int(input("Starting Frame: "))
total_frames = int(input("Total Frames: "))

mt = MT.MT(seed)
mt.advance(starting_frame)
rngList = RNGPool.RNGList(mt,128)

def rand(n):
    return (rngList.getValue()*n>>32) & 0xFFFFFFFF

for frame in range(total_frames):
    rngList.advanceFrames(60)
    for i in range(5):
        rngList.getValue()
        EC = rngList.getValue()
        PID = rngList.getValue()
        IVs = [0]*6
        for c in range(6):
            if IVs[c] == 0:
                IVs[c] = rngList.getValue() >> 27
        print(frame+starting_frame,i+1,hex(PID), hex(EC), *IVs, sep=", ")
        rngList.getValue()
        rngList.getValue()
    rngList.advanceState()
    