# LCRNG Classes

class LCRNG:
    # template
    mult = 0x0
    add = 0x0
    reversed = False
    size = 32

    def __init__(self, seed):
        # lazy way of generating bit mask
        self.mask = (2 << (self.size - 1)) - 1
        # reverse if needed
        if self.reversed:
            self.mult, self.add = self.reverse()
        self.seed = seed

    def reverse(self):
        # extended euclids algorithm thing to get your reverse mult
        def find_reverse_mult(mult, limit): 
            if mult == 0:
                return 0,1
            x1,y1 = find_reverse_mult(limit%mult, mult)
            x = y1 - (limit//mult) * x1
            y = x1
            
            return x,y

        # simple way to find the reverse add, this effectively subtracts the normal add after being multiplied by the reverse_mult
        def find_reverse_add(add,reverse_mult):
            return ((-add * reverse_mult) & self.mask)

        reverse_mult, _ = find_reverse_mult(self.mult, self.mask + 1)
        reverse_mult &= self.mask
        reverse_add = find_reverse_add(self.add, reverse_mult)

        return reverse_mult, reverse_add

    def next(self):
        self.seed = (self.seed * self.mult + self.add) & self.mask
        return self.seed

    def nextHigh(self, size = 16):
        # get highest bits of size
        return self.next() >> (self.size-size)

    def nextFloat(self, size = 16):
        # divide by max + 1 to get a float
        return self.nextHigh(size) / (2<<size)

    def advance(self, advances):
        for _ in range(advances):
            self.next()

# set up specific lcrngs
class PokeRNG(LCRNG):
    mult = 0x41c64e6d
    add = 0x6073

class PokeRNGR(PokeRNG):
    reversed = True
            
class XDRNG(LCRNG):
    mult = 0x343FD
    add = 0x269EC3

class XDRNGR(XDRNG):
    reversed = True

class ARNG(LCRNG):
    mult = 0x6c078965
    add = 1

class ARNGR(ARNG):
    reversed = True
        
class MRNG(LCRNG):
    mult = 0x41C64E6D
    add = 0x3039
        
class MRNGR(MRNG):
    reversed = True

class BTPlay(LCRNG):
    mult = 0x2E90EDD
    add = 1

class BTPlayR(BTPlay):
    reversed = True

class BTDay(LCRNG):
    mult = 0x5D588B65
    add = 1

class BTDayR(BTDay):
    reversed = True