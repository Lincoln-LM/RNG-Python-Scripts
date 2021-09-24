from TinyTimeline import TinyTimeline
advances = 0
index = 0
state = [0xC5AC44ED,0x316727AD,0x77FE69BB,0x6BFBE324]
# tiny_advancer[0] = type 
# tiny_advancer[1] = advance
tiny_advancers = [[7,0],[7,2],[7,4],[7,6]]
ttt = TinyTimeline(initial_state=state,advances=advances,index=index,tiny_advancers=tiny_advancers)
print(f"Start\t~\tEnd \tIndex \tState")
for _ in range(56):
    time = ttt.next_time()
    print(f"{time[0]}\t~\t{time[1]} \t{time[2]} \t{time[6]:08X},{time[5]:08X},{time[4]:08X},{time[3]:08X}")