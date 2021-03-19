# Script to read TinyMT Seeds from 3ds memory

from time import sleep
from PyNTR import PyNTR

c = PyNTR("192.168.0.28") # my console ip
c.start_connection()
c.set_game_name("sango-1") # omega rubys name [x,y,or,as] = [kujira-1, kujira-2, sango-1, sango-2]
c.start_debug_connection()
c.resume()

last_tiny_seeds = []
seeds = []
first = True
rng = False
while True:
    tiny_seeds = []
    for index in range(4):
        tiny_seeds.append(c.ReadU32(0x08c59E04+(index*4))) # reads from oras index 0x08c52808 is for xy
    if tiny_seeds != last_tiny_seeds and not first:
        print("Current Seeds:")
        for i in range(3,-1,-1):
            print("["+str(i)+"] "+hex(tiny_seeds[i])[2:].zfill(8))
        last_tiny_seeds = tiny_seeds
    if first:
        first = False
        seeds = tiny_seeds
        print("Initial Seeds:")
        for i in range(3,-1,-1):
            print("["+str(i)+"] "+hex(tiny_seeds[i])[2:].zfill(8))
        last_tiny_seeds = tiny_seeds

    sleep(0.3)