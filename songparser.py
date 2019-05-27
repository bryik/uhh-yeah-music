import json
import re
from functools import reduce


def processSong(song):
    if song is None:
        return None

    # Pattern 1
    # Song // Artist // Album
    p1 = re.match(r"(.*)//(.*)//(.*)", song, re.UNICODE)
    if p1:
        title = p1.group(1).strip()
        artist = p1.group(2).strip()
        album = p1.group(3).strip()
        return {"title": title, "artist": artist, "album": album}

    # Pattern 2
    # Song // Artist
    p2 = re.match(r"(.*)//(.*)", song, re.UNICODE)
    if p2:
        title = p2.group(1).strip()
        artist = p2.group(2).strip()
        return {"title": title, "artist": artist}

    # TODO: is just a song enough?
    return None


def processEpisode(episode):
    episode["intro"] = processSong(episode["intro"])
    episode["outro"] = processSong(episode["outro"])
    return episode


def main():
    with open("uym.json") as inputfile:
        uym = json.load(inputfile)

    uym = list(map(processEpisode, uym))

    # Extract songs.
    def songReducer(acc, curr):
        acc.append(curr["intro"])
        acc.append(curr["outro"])
        return acc

    uym = reduce(songReducer, uym, [])

    # Remove nulls
    uym = [s for s in uym if s is not None]

    with open("uym-songs.json", "w") as outputfile:
        json.dump(uym, outputfile, ensure_ascii=False)


main()
