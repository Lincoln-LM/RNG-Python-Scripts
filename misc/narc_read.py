"""Functions for reading information from narc files"""

class SmartByteArray:
    """Simple bytearray wrapper that allows getting specific len ints at specific positions"""
    def __init__(self, data, endianess='little'):
        self.data = data
        self.endianess = endianess

    def get_int(self, position, length):
        """Wrapper around int.from_bytes that references the internal bytearray"""
        return int.from_bytes(self.data[position:position+length],self.endianess)

def get_int(_bytes, endianess='little'):
    """Simple wrapper around int.from_bytes"""
    return int.from_bytes(_bytes, endianess)

def read_narc(name, index):
    """Read index from narc file"""
    with open(name, "rb") as file:
        file.seek(12)
        fat_top = get_int(file.read(2))
        file.seek(fat_top + 4)
        size = get_int(file.read(4))
        # file_cnt =
        get_int(file.read(2))
        fnt_top = fat_top + size
        file.seek(fnt_top + 4)
        img_top = fnt_top + get_int(file.read(4))

        file.seek(fat_top + 12 + index * 8)
        top = get_int(file.read(4))
        bottom = get_int(file.read(4))

        file.seek(img_top + 8 + top)

        data = file.read(bottom - top)
        return data
