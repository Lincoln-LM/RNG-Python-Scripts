# Script to get position in the tinymtrng a given state is

import TinyMT

print("Initial Seeds:")
initial_state = []
for i in range(3,-1,-1):
    initial_state.append(int(input("["+str(i)+"]: 0x"),16))
initial_state.reverse()

print("Target Seeds:")
target_state = []
for i in range(3,-1,-1):
    target_state.append(int(input("["+str(i)+"]: 0x"),16))
target_state.reverse()

tmt = TinyMT.TinyMT(state=initial_state)
frame = 0
while tmt.state != target_state:
    print(frame,hex(tmt.next()),*tmt.display_state())
    frame += 1
print(frame,*tmt.display_state())