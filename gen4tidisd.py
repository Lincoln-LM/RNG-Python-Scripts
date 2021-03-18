# quick script to show the tid/sid you get from a seed

import MT

seed = int(input("Seed: 0x"),16)

mt = MT.MT(seed)
mt.next()
sidtid = mt.next()
sid = sidtid >> 16
tid = sidtid & 0xFFFF

print("TID: ",tid,"SID: ", sid)