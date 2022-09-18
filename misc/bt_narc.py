import json
from narc_read import SmartByteArray, read_narc

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
