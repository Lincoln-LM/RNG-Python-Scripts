from LCRNG import BTDay, BTPlay
import json
with open("dp_bt_trainer_names.txt") as trainer_names_file:
    TRAINER_NAMES = trainer_names_file.read().split("\n")
with open("dp_bt_trainer_data.json") as trainer_info_file:
    TRAINER_INFO = json.load(trainer_info_file)

def is_shiny(tid,sid,pid):
    return ((pid >> 16) ^ (pid & 0xFFFF) ^ tid ^ sid) < 8

TRAINER_RANGES = [[  1-1,100-1],
                  [ 81-1,120-1],
                  [101-1,140-1],
                  [121-1,160-1],
                  [141-1,180-1],
                  [161-1,200-1],
                  [181-1,220-1],
                  [201-1,300-1]]
FINAL_TRAINER_RANGES = [[101-1,120-1],
                        [121-1,140-1],
                        [141-1,160-1],
                        [161-1,180-1],
                        [181-1,200-1],
                        [201-1,220-1],
                        [221-1,240-1],
                        [201-1,300-1]]
TOWER_MASTER_FIRST = 305
TOWER_MASTER_SECOND = 306

def generate(btday_seed,stage,forfeit=False,all_rounds=True):
    if forfeit:
        btday_seed = BTDay(btday_seed).next()
    rng = BTPlay(btday_seed)
    rng.advance(24 * stage)
    rng.next()
    stage_trainers = []
    for current_round in range(7):
        trainer_data = trainer_name = None
        while trainer_data is None or (trainer_data,trainer_name) in stage_trainers:
            if stage == 2 and current_round == 6:
                trainer = TOWER_MASTER_FIRST
            elif stage == 6 and current_round == 6:
                trainer = TOWER_MASTER_SECOND
            else:
                if stage < 7 and current_round == 6:
                    trainer = ((rng.next() // 65535) % (FINAL_TRAINER_RANGES[stage][1] - FINAL_TRAINER_RANGES[stage][0] + 1)) + FINAL_TRAINER_RANGES[stage][0]
                else:
                    trainer = ((rng.next() // 65535) % (TRAINER_RANGES[stage][1] - TRAINER_RANGES[stage][0] + 1)) + TRAINER_RANGES[stage][0]
            trainer_data = TRAINER_INFO[trainer]
            trainer_name = TRAINER_NAMES[trainer]
        stage_trainers.append((trainer_data,trainer_name))
    for current_round in range(7 if all_rounds else 1):
        trainer_data,trainer_name = stage_trainers[current_round]
        pokemon_list = []
        while len(pokemon_list) < 3:
            pokemon = (rng.next() // 65535) % len(trainer_data)
            if trainer_data[pokemon] in pokemon_list or any(trainer_data[mon]["item"] == trainer_data[pokemon]["item"] for mon in pokemon_list):
                continue
                    
            pokemon_list.append(pokemon)
        tid = rng.next() // 65535
        sid = rng.next() // 65535
        print(f"{current_round=}")
        print(f"{trainer_name=}")
        print(f"{tid=} {sid=}")
        for pokemon in pokemon_list:
            pokemon_data = trainer_data[pokemon]
            nature = pokemon_data["nature"]
            pid = None
            while pid is None or (pid % 25 != nature and is_shiny(tid,sid,pid)):
                pid = (rng.next() // 65535) | (rng.next() // 65535) << 16
            shiny = is_shiny(tid,sid,pid)
            pokemon_name = pokemon_data["species"]
            print(f"{pokemon_name=} {shiny=} {pid=:08X}")
        print()
        rng.next()

generate(0x00001FC6,0,forfeit=False,all_rounds=True)
