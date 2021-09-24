# Used to get seed from PID/IVs

class RNGCache:
    def __init__(self):
        self.low = []
        self.flags = []

        for _ in range(0x10000):
            self.low.append(0)
            self.flags.append(False)

        self.k = 0xC64E6D00
        self.mult = 0x41c64e6d
        self.add = 0x6073
        for i in range(256):
            right = (self.mult * i + self.add) & 0xFFFFFFFF
            val = (right >> 16) & 0xFFFF
            self.flags[val] = True
            self.low[val] = i & 255
            val -= 1
            self.flags[val] = True
            self.low[val] = i & 255

    def recoverLower16BitsPID(self, pid):
        first = (pid << 16) & 0xFFFFFFFF
        second = pid & 0xFFFF0000
        search = (second - (first * self.mult)) & 0xFFFFFFFF
        origin = []
        for i in range(256):
            if self.flags[search >> 16]:
                test = first | (i << 8) | self.low[search >> 16]
                if ((test * self.mult + self.add) & 0xffff0000) == second:
                    origin.append(test)
            search = (search-self.k) & 0xFFFFFFFF
        
        return origin

    def recoverLower16BitsIV(self, hp, atk, defe, spa, spd, spe):
        first = (((hp | (atk << 5) | (defe << 10)) << 16)) & 0xFFFFFFFF
        second = (((spe | (spa << 5) | (spd << 10)) << 16)) & 0xFFFFFFFF

        search1 = (second - (first * self.mult)) & 0xFFFFFFFF
        search2 = (second - ((first ^ 0x80000000) * self.mult)) & 0xFFFFFFFF


        origin = []
        for i in range(256):
            if self.flags[search1 >> 16]:
                test = first | (i << 8) | self.low[search1 >> 16]
                if ((test * self.mult + self.add) & 0x7fff0000) == second:
                    origin.append(test)

            if self.flags[search2 >> 16]:
                test = first | (i << 8) | self.low[search2 >> 16]
                if ((test * self.mult + self.add) & 0x7fff0000) == second:
                    origin.append(test)
            
            search1 = (search1-self.k) & 0xFFFFFFFF
            search2 = (search2-self.k) & 0xFFFFFFFF
        
        return origin