"""
Calculating the time needed to get a checksum for wishmaker jirachi
messy, not fully working, don't use
"""

checksum = 0x3248
target = 0x261d
hours = 0
minutes = 18
seconds = 28
frames = 46
def u32tou16(val):
    val = val & 0xFFFFFFFF
    val1 = val >> 16
    val2 = val & 0xFFFF
    return (val1 + val2) & 0xFFFF
timecheck = u32tou16((minutes + (seconds << 8)) + (frames << 16))
timelesscheck = (checksum-timecheck) & 0xFFFF
timefortarget = (target-timelesscheck) & 0xFFFF
if (timefortarget >> 8) < 59:
    if (timefortarget & 0xFF) < 59+59:
        print("POSSIBLE")
print(f"{(timefortarget & 0xFF)//2}:{timefortarget >> 8}:{(timefortarget & 0xFF)-((timefortarget & 0xFF)//2)}")
print(f"{timefortarget:04X}")
sanity = (timefortarget+timelesscheck) & 0xFFFF
for minute in range(0,60):
    for second in range(0,60):
        for frame in range(0,60):
            if (u32tou16((minute + (second << 8)) + (frame << 16)) + timelesscheck) & 0xFFFF == target:
                print(f"{(u32tou16((minute + (second << 8)) + (frame << 16)) + timelesscheck) & 0xFFFF:04X}")
                print(f"{minute}:{second}:{frame}")
print(f"{(u32tou16((minute + (second << 8)) + (frame << 16)) + timelesscheck) & 0xFFFF:04X}")
print(f"{minute}:{second}:{frame}")
print(f"{sanity:04X} {target:04X}")
