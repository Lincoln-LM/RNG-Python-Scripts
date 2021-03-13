# Proof of concept script to show how to search for multi shiny hordes, extremely slow since python

import MT
import RNGPool
import math

starting_seed = int(input("Starting Seed: 0x"),16)
last_seed = int(input("Last Seed: 0x"),16)
total_frames = int(input("Total Frames: "))
min_shinies = int(input("Minimum Shinies: "))

for seed in range(starting_seed,last_seed+1):
    mt = MT.MT(seed)
    rngList = RNGPool.RNGList(mt,128)
    def rand(n):
        return (rngList.getValue()*n>>32) & 0xFFFFFFFF
    for frame in range(total_frames):
        rngList.advanceFrames(60)
        scount = 0
        for i in range(5):
            rngList.getValue()
            EC = rngList.getValue()
            PID = rngList.getValue()
            pidhigh = PID>>16
            pidlow = PID&0xFFFF
            if i == 0:
                target_psv = math.floor((pidhigh^pidlow)/8)
            else:
                if target_psv == math.floor((pidhigh^pidlow)/8):
                    scount += 1
            IVs = [0]*6
            for c in range(6):
                if IVs[c] == 0:
                    IVs[c] = rngList.getValue() >> 27
            if scount >= min_shinies:
                print(hex(seed),frame,i+1,hex(PID), hex(EC), *IVs, sep=", ")
            rngList.getValue()
            rngList.getValue()
        rngList.advanceState()
    