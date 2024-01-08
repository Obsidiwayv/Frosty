import base64
import json
from io import BytesIO

import dragon.gd.gd_constants
import dragon.gd.official_songs
import dragon.gd.colours

with open("./dragon/gd/json/colors.json") as colour_json:
    colors = json.load(colour_json)


def user_scores(user: str):
    s = user.split(":")
    return {
        "name": s[1],
        "playerID": int(s[3]),
        "accountID": int(s[21]),
        "rank": int(s[9]),
        "stars": int(s[23]),
        "diamonds": int(s[29]),
        "secretCoins": int(s[5]),
        "userCoins": int(s[7]),
        "demons": int(s[31]),
        "moons": int(s[25]),
        "creatorPoints": int(s[27]),
        "c1": dragon.gd.colours.rgb_to_hex(colors[s[13]]),
        "c2": dragon.gd.colours.rgb_to_hex(colors[s[15]]),
        "iconType": dragon.gd.gd_constants.Icon.objects[s[17]]
    }


def level_data(res: str):
    levels = res.split("#")[0].split("|")
    creators = res.split("#")[1].split("|")
    songs = res.split("#")[2].split("~:~")

    level_output = []
    enc_creators = {}
    enc_songs = {}

    for creator in creators:
        player_id = creator.split(":")[0]
        username = creator.split(":")[1]
        enc_creators[player_id] = username

    for song in songs:
        if song != '':
            sp = song.split("~|~")
            song_id = sp[1]
            song_name = sp[3]
            song_artist_id = sp[5]
            song_artist = sp[7]
            size = sp[9]
            link = sp[13]

            enc_songs[song_id] = {
                "name": song_name,
                "id": int(song_id),
                "artist": song_artist,
                "artistId": int(song_artist_id),
                "file_size": f"{size} MB",
                "link": link
            }

    for lvl in levels:
        level_object = lvl.split(":")

        difficulties = dragon.gd.gd_constants.Difficulty.basic

        if level_object[21] != '':
            if bool(int(level_object[21])):
                difficulties = dragon.gd.gd_constants.Difficulty.demons

        output = {
            "id": int(level_object[1]),
            "name": level_object[3],
            "levelVersion": int(level_object[5]),
            "playerID": int(level_object[7]),
            "description": base64.b64decode(level_object[35]).decode("utf-8")
            if level_object[35] != '' else "No Description",
            "difficulty": difficulties[int(level_object[11])],
            "stars": int(level_object[27]),
            "downloads": int(level_object[13]),
            "likes": int(level_object[19]),
            "disliked": True if int(level_object[19]) < 0 else False,
            "length": dragon.gd.gd_constants.Length.objects[int(level_object[37])],
            "demon": is_demon(level_object[21]),
            "featured": bool(int(level_object[29])),
            "epic": bool(int(level_object[31])),
            "objects": int(level_object[33]),
            "stars_requested": int(level_object[47]),
            "game_version": dragon.gd.gd_constants.Version.lists[int(level_object[17])] if
            dragon.gd.gd_constants.Version.lists[int(level_object[17])] else "Pre-1.7",
            "copied_from": int(level_object[39]),
            "large": True if int(level_object[33]) > 4e4 else False,
            "two_player": bool(int(level_object[41])),
            "coins": int(level_object[43]),
            "verified_coins": bool(int(level_object[45]))
        }

        official_song_id = int(int(level_object[15]))
        song_id = int(level_object[53])
        player_id = level_object[7]
        song = None

        if official_song_id == 0 and song_id != 0 or official_song_id != 0 and song_id != 0:
            song = enc_songs[str(song_id)]
        if official_song_id != 0 and song_id == 0:
            song = dragon.gd.official_songs.get_song(official_song_id + 1)
        if official_song_id == 0 and song_id == 0:
            song = dragon.gd.official_songs.get_song(1)

        output["creator"] = enc_creators[player_id] if enc_creators.get(player_id) else "-"
        output["song"] = song

        level_output.append(output)

    return level_output


def is_demon(code: str):
    if code == '':
        return False
    else:
        return bool(int(code))
