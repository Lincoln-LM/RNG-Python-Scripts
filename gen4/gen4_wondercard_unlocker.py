class ByteStruct(object):
    def __init__(self, buf):
        # read buf from file
        if isinstance(buf, str):
            with open(buf,"rb") as file:
                buf = file.read()
        self.data = bytearray(buf[:])

    def get_u64(self, offset):
        return self.get_int(offset, 8)

    def get_u32(self, offset):
        return self.get_int(offset, 4)

    def get_u16(self, offset):
        return self.get_int(offset, 2)

    def get_u8(self, offset):
        return self.get_int(offset, 1)

    def set_u64(self, num, offset):
        return self.set_int(num, offset, 8)

    def set_u32(self, num, offset):
        return self.set_int(num, offset, 4)

    def set_u16(self, num, offset):
        return self.set_int(num, offset, 2)

    def set_u8(self, num, offset):
        return self.set_int(num, offset, 1)

    def get_string(self, offset, size):
        return self.data[offset:offset+size].decode("utf-16").rstrip('\x00')

    def get_int(self, offset, size):
        return int.from_bytes(self.data[offset:offset + size], byteorder='little')

    def set_int(self, num, offset, size):
        self.data[offset:offset + size] = int.to_bytes(num, size, byteorder='little')
    
    def save(self, name):
        with open(name, "wb+") as file:
            file.write(self.data)

class PK4(ByteStruct):
    STOREDSIZE = 136
    PARTYSIZE = 236
    BLOCKSIZE = 32

    def __init__(self,buf):
        self.data = bytearray(buf[:])
        self.decrypt()

    @property
    def pid(self):
        return self.get_u32(0x0)
    
    @pid.setter
    def pid(self, value):
        self.set_u32(value,0x0)

    @property
    def checksum(self):
        return self.get_u16(0x6)

    @property
    def species(self):
        return self.get_u16(0x8)

    def calc_checksum(self):
        chk = 0
        for i in range(8,PK4.STOREDSIZE,2):
            chk += self.get_u16(i)
            chk &= 0xFFFF
        return chk

    def decrypt(self):
        seed = self.pid
        sv = (seed >> 13) & 0x1F

        self.__cryptPKM__(seed,self.checksum)
        self.__shuffle__(sv)
    
    def __cryptPKM__(self,seed,checksum):
        self.__crypt__(checksum, 8, PK4.STOREDSIZE)
        if len(self.data) > PK4.STOREDSIZE:
            self.__crypt__(seed, PK4.STOREDSIZE, len(self.data))

    def __crypt__(self, seed, start, end):
        i = start
        while i < end:
            seed = seed * 0x41C64E6D + 0x00006073
            self.data[i] ^= (seed >> 16) & 0xFF
            i += 1
            self.data[i] ^= (seed >> 24) & 0xFF
            i += 1

    def __shuffle__(self, sv):
        idx = 4 * sv
        sdata = bytearray(self.data[:])
        for block in range(4):
            ofs = PK4.BLOCKPOSITION[idx + block]
            self.data[8 + PK4.BLOCKSIZE * block : 8 + PK4.BLOCKSIZE * (block + 1)] = sdata[8 + PK4.BLOCKSIZE * ofs : 8 + PK4.BLOCKSIZE * (ofs + 1)]

    def refresh_checksum(self):
        self.set_u16(self.calc_checksum(),0x6)

    def encrypt(self):
        self.refresh_checksum()
        seed = self.pid
        sv = (seed >> 13) & 0x1F

        self.__shuffle__(PK4.BLOCKPOSITIONINVERT[sv])
        self.__cryptPKM__(seed,self.checksum)
        return self.data

    BLOCKPOSITIONINVERT = [
            0, 1, 2, 4, 3, 5, 6, 7, 12, 18, 13, 19, 8, 10, 14, 20, 16, 22, 9, 11, 15, 21, 17, 23,
            0, 1, 2, 4, 3, 5, 6, 7,
    ]

    BLOCKPOSITION = [
        0, 1, 2, 3,
        0, 1, 3, 2,
        0, 2, 1, 3,
        0, 3, 1, 2,
        0, 2, 3, 1,
        0, 3, 2, 1,
        1, 0, 2, 3,
        1, 0, 3, 2,
        2, 0, 1, 3,
        3, 0, 1, 2,
        2, 0, 3, 1,
        3, 0, 2, 1,
        1, 2, 0, 3,
        1, 3, 0, 2,
        2, 1, 0, 3,
        3, 1, 0, 2,
        2, 3, 0, 1,
        3, 2, 0, 1,
        1, 2, 3, 0,
        1, 3, 2, 0,
        2, 1, 3, 0,
        3, 1, 2, 0,
        2, 3, 1, 0,
        3, 2, 1, 0,

        # duplicates of 0-7 to eliminate modulus
        0, 1, 2, 3,
        0, 1, 3, 2,
        0, 2, 1, 3,
        0, 3, 1, 2,
        0, 2, 3, 1,
        0, 3, 2, 1,
        1, 0, 2, 3,
        1, 0, 3, 2,
    ]

class MysteryGift(ByteStruct):
    def __init__(self, buf):
        ByteStruct.__init__(self, buf)
        self.pokemon = PK4(self.data[8 : PK4.PARTYSIZE + 8])

    def update(self):
        self.data[8 : PK4.PARTYSIZE + 8] = self.pokemon.encrypt()

mg = MysteryGift("XXXXX.pgt") # can be .pgt or .pcd
mg.pokemon.pid = 0
mg.update()
mg.save("XXXXX.pgt") # can be .pgt or .pcd