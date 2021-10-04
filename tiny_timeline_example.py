from TinyTimeline import TinyTimeline
from TinyMT import TinyMT
index = 4293
initial_state = [0x114D3525,0x66C2F888,0xC572CFAD,0x1EB60DB7]
# tiny_advancer[0] = type 
# tiny_advancer[1] = advance
tiny_advancers = [[6,28271,False]]
ttt = TinyTimeline(initial_state=initial_state,index=index,tiny_advancers=tiny_advancers)
print(f"Start\t~\tEnd \tIndex \tState")
for _ in range(30):
    time = ttt.next_time()
    tmt = TinyMT(state=time[3:7])
    print(((tmt.next() * 100) >> 32) & 0xFFFFFFFF)
    if time[1] <= time[0]:
        print(f"-\t~\t- \t{time[2]} \t{time[6]:08X},{time[5]:08X},{time[4]:08X},{time[3]:08X}")
    else:
        print(f"{time[0]}\t~\t{time[1]} \t{time[2]} \t{time[6]:08X},{time[5]:08X},{time[4]:08X},{time[3]:08X}")