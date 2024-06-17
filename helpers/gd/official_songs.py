import json

with open("./helpers/gd/json/officialsongs.json") as official:
    song_json = json.load(official)

song_object = {
    1: song_json["sm"],
    2: song_json["bot"],
    3: song_json["pg"],
    4: song_json["dout"],
    5: song_json["bab"],
    6: song_json["clg"],
    7: song_json["j"],
    8: song_json["tm"],
    9: song_json["c"],
    10: song_json["xs"],
    11: song_json["cf"],
    12: song_json["toe"],
    13: song_json["ea"],
    14: song_json["cs"],
    15: song_json["ed"],
    16: song_json["hf"],
    17: song_json["bp"],
    18: song_json["toeii"],
    19: song_json["gd"],
    20: song_json["d"],
    21: song_json["fd"],
    22: song_json["dash"],
    23: song_json["exp"],
    24: song_json["tss"],
    25: song_json["va"],
    26: song_json["ar"],
    27: song_json["tc"],
    28: song_json["p"],
    29: song_json["bm"],
    30: song_json["m"],
    31: song_json["y"],
    32: song_json["f"],
    33: song_json["sp"],
    34: song_json["s"],
    35: song_json["e"],
    36: song_json["round"],
    37: song_json["mdo"],
    38: song_json["ps"],
    39: song_json["ne"],
    40: song_json["pt"]
}


def get_song(name: int):
    result = song_object[name]
    if not result:
        result = song_json["unknown"]
    return result
