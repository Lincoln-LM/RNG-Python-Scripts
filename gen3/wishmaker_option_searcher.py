"""
Searching all permutations of settings for a wishmaker jirachi checksum
not fully working
"""

import progressbar

gender_dict = {0x0:"Male",0x1:"Female"}
clock_dict = {0x1:"00:00",0x180000:"XX:00",0x3C170000:"XX:XX"}
starter_dict = {(0x08000000 + 0x40000000 + 0x08000000):"Treecko",(0x40000000 + 0x2 + 0x40000000):"Torchic",(0x2 + 0x08000000 + 0x2):"Mudkip"}
text_dict = {0x0:"Slow",0x1:"Medium",0x2:"Fast"}
scene_dict = {0x0:"On",0x400:"Off"}
style_dict = {0x0:"Shift",0x200:"Set"}
sound_dict = {0x0:"Mono",0x100:"Stereo"}
button_dict = {0x0:"Normal",0x1000000:"LR",0x2000000:"L=A"}
frame_dict = {0:"1",0x8:"2",0x10:"3",0x18:"4",0x20:"5",0x28:"6",0x30:"7",0x38:"8",0x40:"9",0x48:"10",0x50:"11",0x58:"12",0x60:"13",0x68:"14",0x70:"15",0x78:"16",0x80:"17",0x88:"18",0x90:"19",0x98:"20"}

max_count = 20*3*2*2*2*3
total_count = 0


def u32tou16(val):
    val = val & 0xFFFFFFFF
    val1 = val >> 16
    val2 = val & 0xFFFF
    return (val1 + val2) & 0xFFFF

def nametovalue(name):
    tvalue = 4278190080
    num = 0
    chartohex = {'A': 187, 'B': 188, 'C': 189, 'D': 190, 'E': 191, 'F': 192, 'G': 193, 'H': 194, 'I': 195, 'J': 196, 'K': 197, 'L': 198, 'M': 199, 'N': 200, 'O': 201, 'P': 202, 'Q': 203, 'R': 204, 'S': 205, 'T': 206, 'U': 207, 'V': 208, 'W': 209, 'X': 210, 'Y': 211, 'Z': 212, 'a': 213, 'b': 214, 'c': 215, 
'd': 216, 'e': 217, 'f': 218, 'g': 219, 'h': 220, 'i': 221, 'j': 222, 'k': 223, 'l': 224, 'm': 225, 'n': 226, 'o': 227, 'p': 228, 'q': 229, 'r': 230, 's': 231, 't': 232, 'u': 233, 'v': 234, 'w': 235, 'x': 236, 'y': 237, 'z': 238, ' ': 0, '．': 173, '，': 184, '0': 161, '1': 162, '2': 163, '3': 164, '4': 165, '5': 166, '6': 167, '7': 168, '8': 169, '9': 170, '！': 171, '？': 172, '♂': 181, '♀': 182, '／': 186, '－': 174, '‥': 176, '“': 177, '”': 178, '‘': 179, '’': 11}
    while num <= 6:
        if (num < len(name)):
            tvalue = (tvalue) + (chartohex[name[num]] << (num % 4) * 8) & 0xFFFFFFFF
        else:
            tvalue = (tvalue) + (255 << (num % 4) * 8) & 0xFFFFFFFF
        num += 1
    return tvalue

def gen(cur, val, start, end, arr, target, star):
    if start == end:
        global c, min_mf, min_s
        val = u32tou16(val+star)
        if val not in c:
            global close
            c.append(val)
            if close[0] < val <= (target - min_mf - min_s*0x100)&0xFFFF:
                close = (val, cur)
                return cur
        return ""

    choices = arr[start]
    final = []
    for item in choices:
        a = gen(cur+[item], val+item, start+1, end, arr, target, star)
        if a != "":
            final.append(a)
            
    if final != []:
        return final
    return ""

lis1 = [
    [0,0x1,0x2],
    [0,0x400],
    [0,0x200],
    [0,0x100],
    [0,0x1000000,0x2000000],
    [0,0x8,0x10,0x18,0x20,0x28,0x30,0x38,0x40,0x48,0x50,0x58,0x60,0x68,0x70,0x78,0x80,0x88,0x90,0x98]
]

titles = ["Text Speed:","Battle Scene:","Battle Style:","Sound:","Button Mode:","Frame Type:"]
titles2 = []
dicts = [text_dict,scene_dict,style_dict,sound_dict,button_dict,frame_dict]
dicts2 = []
m2 = []

c = []
close = (0, [])

start = 0x10
attr = []
print("---Search Settings---")
genderS = int(input("Include Gender? (1/0):"))
clockS = int(input("Include Clock Settings? (1/0):"))
starterS = int(input("Include Starters? (1/0):"))
tid = int(input("TID:"))
sid = int(input("SID:"))
name = input("Name:")

n = name
name = nametovalue(name)
print(hex(name))

attr.append(tid<<16)
attr.append(sid)
attr.append(name)

if not genderS:
    gender = int(input("Gender (0=M 1=F):"))
    attr.append(gender)
    titles2.append("Gender:")
    dicts2.append(gender_dict)
    m2.append(gender)
else:
    max_count *= 2
    lis1.append([0,1])
    titles.append("Gender:")
    dicts.append(gender_dict)

if not clockS:
    clock = int(input("Clock Settings (0=00:00 1=XX:00 2=XX:XX):"))

    if clock == 0:
        clock = 0x0
    elif clock == 1:
        clock = 0x180000
    else:
        clock = 0x3C170000

    attr.append(clock)
    titles2.append("Clock Settings:")
    dicts2.append(clock_dict)
    m2.append(clock)
else:
    max_count *= 3
    lis1.append([1,0x180000,0x3C170000])
    titles.append("Clock Settings:")
    dicts.append(clock_dict)

if not starterS:
    starter = int(input("Starter (0=Treecko 1=Torchic 2=Mudkip):"))

    if starter == 0:
        starter = 0x08000000 + 0x40000000 + 0x08000000
    elif starter == 1:
        starter = 0x40000000 + 0x2 + 0x40000000
    else:
        starter = 0x2 + 0x08000000 + 0x2

    attr.append(starter)
    titles2.append("Starter:")
    dicts2.append(starter_dict)
    m2.append(starter)

else:
    max_count *= 3
    lis1.append([0x08000000 + 0x40000000 + 0x08000000,0x40000000 + 0x2 + 0x40000000,0x2 + 0x08000000 + 0x2])
    titles.append("Starter:")
    dicts.append(starter_dict)

for at in attr:
    start += at

min_time = [int(x) for x in (input("Min Time (MM:SS:FF): ").split(":"))]
max_time = [int(x) for x in (input("Max Time (MM:SS:FF): ").split(":"))]

min_mf = min_time[0]
min_s = 0 if min_time[0] != 59 else min_time[1]

target = int(input("Target Seed: 0x"), 16)

diff = target
found = True
gen([],0,0,len(lis1),lis1,diff,start)
with progressbar.ProgressBar(max_value=max_count) as bar:
    total_count += 1
    bar.update(total_count)
    while ((diff-close[0]) % 0x100 > 118) | ((diff-close[0]) // 0x100 > 59) | ((diff-close[0]) % 0x100 < min_mf) | ((diff-close[0]) // 0x100 < min_s):
        g = close[0]-1
        c = []
        close = (0, [])
        gen([],0,0,len(lis1),lis1,g,start)
        total_count += 1
        if total_count == max_count:
            found = False
            break
        bar.update(total_count)

if not found:
    print("no possible seeds found with this setup")
    exit(0)

mf = (diff-close[0]) % 0x100
s = (diff-close[0]) // 0x100

print()
print(f"Timeless Seed: {close[0]:04X}")

print()
print("---Checksum Setup Information---")
print("TID:",tid)
print("SID:",sid)
print("Name:",n)

for i in range(len(titles2)):
    print(titles2[i],dicts2[i][m2[i]])

for i in range(len(titles)):
    print(titles[i],dicts[i][close[1][i]])

print()
print("---Time Information---")
print(f"MINUTEFRAME: {mf} SECOND: {s}")
print()
print("Times to hit:")
for minute in range(min_time[0], max_time[0]):
    for second in range(min_time[1] if minute == min_time[0] else 0, max_time[1]+1 if minute == max_time[0] else 60):
        for frame in range(min_time[2] if second == min_time[1] else 0, max_time[2]+1 if minute == max_time[1] else 60):
            if minute + frame == mf and second == s:
                print(f"{minute:02d}:{second:02d}:{frame:02d}")
