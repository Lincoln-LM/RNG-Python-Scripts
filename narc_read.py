import json


class SmartByteArray:
    def __init__(self, data, endianess='little'):
        self.data = data
        self.endianess = endianess
    def get_int(self, position, length):
        return int.from_bytes(self.data[position:position+length],self.endianess)

def get_int(bytes,endianess='little'):
    return int.from_bytes(bytes,endianess)

class B_TOWER_TRAINER_ROM_DATA(SmartByteArray):
    @property
    def tr_type(self):
        return self.get_int(0,2)
    @property
    def use_poke_cnt(self):
        return self.get_int(2,2)
    @property
    def use_poke_table(self):
        table = [self.get_int(position,2) for position in range(4,len(self.data),2) if self.get_int(position,2) != 0]
        return table

class B_TOWER_POKEMON_ROM_DATA(SmartByteArray):
    @property
    def mons_no(self):
        return self.get_int(0,2)
    @property
    def waza(self):
        table = [self.get_int(position,2) for position in range(2,10,2)]
        return table
    @property
    def exp_bit(self):
        return self.get_int(10,1)
    @property
    def chr(self):
        return self.get_int(11,1)
    @property
    def item_no(self):
        return self.get_int(12,2)
    @property
    def dummy(self):
        return self.get_int(14,2)

def read_narc(name, index):
    with open(name, "rb") as file:
        file.seek(12)
        fat_top = get_int(file.read(2))
        file.seek(fat_top + 4)
        size = get_int(file.read(4))
        file_cnt = get_int(file.read(2))
        fnt_top = fat_top + size
        file.seek(fnt_top + 4)
        img_top = fnt_top + get_int(file.read(4))

        file.seek(fat_top + 12 + index * 8)
        top = get_int(file.read(4))
        bottom = get_int(file.read(4))

        file.seek(img_top + 8 + top)

        data = file.read(bottom - top)
        return data

with open("pokemon.txt") as pokemon_names_file:
    POKEMON_NAMES = pokemon_names_file.read().split("\n")
trainer_list = []
for trainer in range(307):
    trainer_data = B_TOWER_TRAINER_ROM_DATA(read_narc("btdtr.narc",trainer))
    pokemon_list = []
    for mon in trainer_data.use_poke_table:
        pokemon_data = B_TOWER_POKEMON_ROM_DATA(read_narc("btdpm.narc",mon))
        pokemon_list.append({"species": POKEMON_NAMES[pokemon_data.mons_no], "nature": pokemon_data.chr, "item": pokemon_data.item_no})
    trainer_list.append(pokemon_list)
json.dump(trainer_list,open("dp_bt_trainer_data.json","w+"))